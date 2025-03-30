from  django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.db import connection


from accounts.models import Post, User, Comment


# Create your views here.

def DisplayAll(req):
    
    islogin = req.session.get('is_authenticated')
    posts = Post.objects.all()
    return render(req, 'DisplayPosts.html', {'data': posts , 'islogin': islogin})
    

def create_post(req):
    islogin = req.session.get('is_authenticated')
    if islogin:
        if req.method == 'POST':
            title = req.POST.get('title')
            content = req.POST.get('content')
            category = req.POST.get('category')
            author_id = req.session.get('user_id')
            
            user = User.objects.get(id =author_id)
        
            with connection.cursor() as conn:
                query = f"INSERT INTO accounts_post (title, content, category, author_id, created_at, updated_at) VALUES ('{title}', '{content}', '{category}', '{author_id}', NOW(), NOW())"
                conn.execute(query)
                print(query)
        
            return redirect('posts')
        return render(req, 'create_post.html', {'islogin': islogin})
    
    else:
        return redirect('login', {'islogin': islogin})


def dispalyPost(req,id):
    islogin = req.session.get('is_authenticated')
    if req.method == 'POST':
        if islogin:
            email = req.session.get('email')
            comment = req.POST.get('comment')
            
            u = User.objects.get(email=email)
            with connection.cursor() as conn:
                query = f"INSERT INTO accounts_comment (content, post_id, user_id, created_at) VALUES ('{comment}', '{id}', '{u.id}', NOW())"
                conn.execute(query)
            return redirect('post', id=id)
        else:
            return redirect('login')
            
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post_id=id)
    userComment = {}
    for e in comments:
        user = User.objects.get(id=e.user_id)
        hiscomments = Comment.objects.filter(user_id=e.user_id, post_id=post.id) 
        
        if e.user_id not in userComment:
            userComment[e.user_id] = {'user': user, 'comments': hiscomments}
    
    return render(req, 'post.html', {'post': post, 'comment': userComment, 'islogin': islogin}) 

    
def my_posts(req):
    islogin = req.session.get('is_authenticated')
    sort_by = req.GET.get('sort', 'title')
    
    if 'date' in sort_by:
        sort_by = 'created_at'
    if not sort_by:
        sort_by='title'
        
    if islogin:
        id_user = req.session.get('user_id')
        with connection.cursor() as con:
            query = f"SELECT * FROM accounts_post WHERE author_id = '{id_user}' ORDER BY {sort_by} DESC"
            con.execute(query)
            #print(query)
            result = con.fetchall()
        return render(req, 'myposts.html', {'posts': result, 'islogin': islogin})
    else:
        return redirect('login') 
  
    
def delete_post(req,id):
    islogin = req.session.get('is_authenticated')
    user_id = req.session.get('user_id')
    if islogin:
        user = User.objects.get(id=user_id)
        post = Post.objects.filter(id=id,author=user)
        if post:
            post.delete()
            messages.success(req, 'Post supprimé avec succès')
        else:
            messages.error(req, 'Post non trouvé')
        return redirect('myPost')
    else:
        return redirect('login')


def edit_post(req, id):
    islogin = req.session.get('is_authenticated')
    
    if islogin:
        newTitle = req.POST.get('title')
        newContent = req.POST.get('content')
        newCategory = req.POST.get('category')
        
        with connection.cursor() as conn:
            query = f"SELECT title, content, category FROM accounts_post WHERE id = '{id}'"
            conn.execute(query)
            result = conn.fetchall() 
            for e in result:
                title = e[0]      
                content = e[1]      
                category = e[2]  
        
        if req.method == 'POST':
            editPost = Post.objects.get(id=id)
            editPost.title = newTitle
            editPost.content = newContent
            editPost.category = newCategory
            editPost.save()
            
            return redirect('myPost')
            
        return render(req, 'editPost.html', {'title': title, 'content': content, 'category':category, 'islogin': islogin})
    else:
        return redirect('login')
        
        
def details(req):
    id = req.GET.get('id')
    islogin = req.session.get('is_authenticated')
    # Define dangerous SQL keywords
    sql_keywords = ['SELECT', 'UNION', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'OR', 'AND','select', 'union', 'insert', 'update', 'delete', 'drop', 'or', 'and']
    
    if islogin:
        author_id = req.session.get('user_id')
        for i in id.split():
            if i in sql_keywords:
                raise Http404("Page not found")
        with connection.cursor() as conn:
            query = f"SELECT * FROM accounts_post WHERE author_id = '{author_id}' AND id = '{id}'"
            conn.execute(query)
            result = conn.fetchall()
            if result:
                return render(req,'details.html', {'islogin': islogin, 'data':result})
            else:
                raise Http404("Page not found")
    else:
        return redirect('login')
          
        
        
        
        
