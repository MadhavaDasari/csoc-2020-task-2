from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from store.models import *
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime 

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    book1=Book.objects.get(pk=bid)
    num_available=BookCopy.objects.filter(status__exact=True,book__exact=book1).count()
    user_rating=0.0
    if(request.user.is_authenticated):
        value= BookRating.objects.filter(book__exact=book1,user__exact=request.user)
        user_rating=0
        if(value.count()>0):
            user_rating=BookRating.objects.filter(book__exact=book1,user__exact=request.user).get().rating

    context = {
        'book': book1, # set this to an instance of the required book
        'num_available':num_available, # set this to the number of copies of the book available, or 0 if the book isn't available
        'user_rating':user_rating,
    }
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    data = request.GET
    books = Book.objects.filter(title__icontains=data.get('title',''),author__icontains=data.get('author',''),genre__icontains=data.get('genre',''))
    context = {
        'books': books, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    # START YOUR CODE HERE   
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    books = BookCopy.objects.filter(borrower__exact=request.user)
    context = {
        'books': books,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE   

    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    book_id = request.POST.get("bid")
    books = BookCopy.objects.filter(book_id__exact=book_id,status__exact=True)
    if(books):
        message = "success"
        books[0].status = False
        books[0].borrower = request.user
        books[0].borrow_date = datetime.date.today()
        books[0].save()
    else :
        message = "failure"
    response_data = {
        'message': message,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE

    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required
def returnBookView(request):
    book_id = request.POST.get("bid")
    book = BookCopy.objects.get(pk=book_id)
    if(book):
      message ="success"
      book.status = True
      book.borrower = None
      book.borrow_date = None
      book.save()
    else :
      message = "failure" 
    response_data = {
        'message': message,
    }
    return JsonResponse(response_data)


@csrf_exempt
@login_required
def userBookRating(request):
    response_data = {
        'message': "failure",
        'rating' : 0 
    }
    prating = '0'
    userid=request.user.id
    data = request.POST
    rating =data.get('rating')
    bookid = data.get('bid')
    print(rating)
    if BookRating.objects.filter(user_id=userid).filter(book_id=bookid).count() == 1:
        prating = BookRating.objects.filter(user_id=userid).filter(book_id=bookid).first().rating
        print('rating')
    if prating == '0':
        rate = BookRating.objects.create(book_id=bookid,user_id=userid,rating=rating)
        response_data['message'] = "success"
    else :
        rate=BookRating.objects.filter(user_id=userid).filter(book_id=bookid).first()
        rate.rating = rating
        rate.save()
        response_data['message'] = "success"
    book=Book.objects.get(id=bookid)
    sum=0
    l= BookRating.objects.filter(book_id=bookid).count()
    for i in range(l):
        rate=BookRating.objects.filter(book_id=bookid)[i]
        sum = sum + int(rate.rating)
    arate=float(sum)/float(l)
    book.rating = round(arate,2)
    book.save()
    response_data['rating'] = book.rating
    return JsonResponse(response_data)
