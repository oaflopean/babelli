from flask import Flask, render_template, request
from flask import render_template, flash, redirect, session, url_for, request, g
#from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
import json
import urllib2
import requests
app = Flask(__name__)
app.config.update(
    PROPAGATE_EXCEPTIONS = True
)


class Book(object):
    def __init__(self, title, author, bookid, textlink, epublink):
        self.title = title
        self.author = author
        self.bookid = bookid
        self.textlink= textlink
        self.epublink = epublink

@app.route('/')
@app.route('/index')
def form():
    gutenberg = json.load(open('gutenberg'))
    ids = json.load(open('ids'))
    authors = json.load(open('authors2'))
    results = []
    tokens = ["prince"]
    IDresults = []
    for g in tokens:
        Ids = []
        try:
            Ids = gutenberg[g]
        except KeyError:
            continue
        try:
            IDresults.extend(Ids)

        except TypeError:
            continue
    Ids = []
    for q in IDresults:
        try:
            try:
                title = ids.get(str(q))

            except KeyError:
                title = "none"
            try:
                author = authors.get(str(q))
            except KeyError:
                author = "none"
            bookid = str(q)
            book = Book(title, author, bookid, "", "")
            linkTxt = "ftp://anonymous@copypastapublishing.com:password@ftp.copypastapublishing.com/gutenberg/"
            epub = linkTxt + "cache/epub/" + str(bookid) + "/"
            formula = list(bookid)
            my_list_len = len(formula)
            for h in range(0, my_list_len - 1):
                linkTxt = linkTxt + "/" + formula[h] + "/"
            linkTxt = linkTxt + bookid
            book.textlink = linkTxt
            book.epublink = epub
            results.append(book)

        except ValueError:
            continue

    return render_template('main.html', query="", results=results)

@app.route('/submitted', methods=['POST'])
def submitted_form():
    query = request.form['search']
    return redirect(url_for('search_results', query=query))


@app.route('/page/<bookid>')
def page(bookid):

    ids = json.load(open("Gutenberg.json"))
    id = ids[bookid]["id"]
    try:
        subject = ids[bookid]["subjects"]
        subject = " ".join(subject).replace(" -- ","\n")
    except TypeError:
        subject = "none"
    try:
        author = ids[bookid]["author"]
    except TypeError:
        author = "none"
    try:
        title = ids[bookid]["title"]
    except TypeError:
        title="none"

    baseLink = "ftp://anonymous@copypastapublishing.com:password@ftp.copypastapublishing.com/gutenberg/"
    httpLink="http://copypastapublishing.com/ftp.copypastapublishing.com/"
    formula = list(bookid)
    my_list_len = len(formula)
    linkTxt = baseLink
    for h in range(0, my_list_len - 1):
        linkTxt = linkTxt + "/" + formula[h] + "/"
    linkTxt = linkTxt + bookid
    for h in range(0, my_list_len - 1):
        httpLink = httpLink + "/" + formula[h] + "/"
    httpLink = httpLink + bookid
    book = Book(title, author, bookid, "", "")
    epub = baseLink + "cache/epub/" + str(bookid) + "/"

    book.textlink = linkTxt
    book.epublink = epub
    result=book
    booktext=""


    data = httpLink + "/"+bookid+".txt"

    return render_template('page_render.html', subject=subject, result=result, data=data)


@app.route('/search_results/<query>')
def search_results(query):
    gutenberg = json.load(open('gutenberg'))
    ids = json.load(open('ids'))
    authors = json.load(open('authors2'))
    results = []
    tokens = query.lower().split(" ")
    IDresults = []
    previous=[]
    if len(tokens)>1:
        for g in tokens:

            Ids=[]
            try:
                Ids = gutenberg[g]
            except KeyError:
                continue
            if IDresults==[]:
                IDresults.extend(Ids)

            try:
                IDresults = set(Ids).intersection(previous)
                if len(IDresults )> 500:
                    break
            except TypeError:
                continue
            previous=Ids
    else:
        try:
            IDresults = gutenberg[tokens[0]]
        except KeyError:
            IDresults=[]

    Ids=[]
    for q in IDresults:
        try:
            try:
                title = ids.get(str(q))
            except KeyError:
                title="none"
            try:
                author = authors.get(str(q))
            except KeyError:
                author="none"
            bookid=str(q)
            book =Book(title, author, bookid,"","")
            baseLink = "ftp://anonymous@copypastapublishing.com:password@ftp.copypastapublishing.com/gutenberg/"
            epub = baseLink + "cache/epub/" + str(bookid)+ "/"
            linkTxt=baseLink
            formula=list(bookid)
            my_list_len=len(formula)
            for h in range(0, my_list_len - 1):
                linkTxt = linkTxt + "/"+formula[h]+"/"
            linkTxt = linkTxt + bookid
            book.textlink = linkTxt
            book.epublink=epub
            results.append(book)

        except ValueError:
            continue


    RESULTS=set(results)
    results=list(RESULTS)
    return render_template('main.html', query=query, results=results)

""" {% {{titles}}[{{title}}] = {{id}}%}
                {% id.split = formula %}
                {% len(formula) = my_list_len   %}
                {% linkTxt= "ftp://ftp.copypastapublishing.com/gutenberg/" %}
                {% for h in range(0, {{my_list_len}} - 1): %}
                {%    linkTxt = linkTxt + formula[h] + "/" %}
                (% endfor %}
                (% {{text}}= linkTxt + id +"/" %}
                (% {{epub}}=linkTxt+"cache/epub/"+id+"/" %}
"""