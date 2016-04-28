# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
flag=2;
def index():
    items_per_page=6
    if len(request.args):
        page=request.args[0]
    else:
        page=0
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    name = db(custom_auth_table.id==auth.user_id).select(custom_auth_table.Name)
    query = db.Meetings.attendees.contains(name) or db.Meetings.minutetaker.contains(name)
    rows=db(query).select(db.Meetings.ALL,limitby=limitby,orderby=~db.Meetings.id)
    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    form=auth()
    return dict(form=form)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

@auth.requires_login()
def minutes():
    items_per_page=6
    if len(request.args):
        page=request.args[0]
    else:
        page=0
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    name = db(custom_auth_table.id==auth.user_id).select(custom_auth_table.Name)
    query = db.Meetings.minutetaker.contains(name)
    rows=db(query).select(db.Meetings.ALL,limitby=limitby,orderby=~db.Meetings.id)
    return locals()

@auth.requires_login()
def searchmeeting():
    return dict(form=FORM(INPUT(_class='inputclass',_id='keyword',_placeholder='Search Other Meetings',_name='keyword',
    _onkeyup="ajax('callback', ['keyword'], 'target')")),
    target_div=DIV(_id='target'))

def callback():
    """an ajax callback that returns a <ul> of links to wiki pages"""
    query = db.Meetings.title.contains(request.vars.keyword) or db.Meetings.tags.contains(request.vars.keyword)
    pages = db(query).select(orderby=~db.Meetings.dt)
    if len(pages):
        links = [(A(p.title,_href=URL('show',args=[p.id,'Meeting'])),XML(' by<BR/>'),A(p.organiser,_href=URL('show',args=[p.id,'Organisation'])),XML(' on<BR/>'),A(p.dt),XML('Tags:<BR/>'),A(p.tags)) for p in pages]
    return DIV(*links)

def searchorg():
    return dict(form=FORM(INPUT(_class='inputclass',_id='keyword',_placeholder='Search Organisations',_name='keyword',
    _onkeyup="ajax('callback1', ['keyword'], 'target')")),
    target_div=DIV(_id='target'))

def callback1():
    """an ajax callback that returns a <ul> of links to wiki pages"""
    query = db.Organisation.name.contains(request.vars.keyword)
    pages = db(query).select(orderby=db.Organisation.name)
    if len(pages):
        if auth.user:
            links = [A(p.name,_href=URL('show',args=[p.id,'Organisation'])) for p in pages]
        else:
            links = [A(p.name) for p in pages]
    return DIV(*links)

@auth.requires_login()
def searchmymeeting():
    return dict(form=FORM(INPUT(_class='inputclass',_id='keyword',_placeholder='Search My Meetings',_name='keyword',
    _onkeyup="ajax('callback2', ['keyword'], 'target')")),
    target_div=DIV(_id='target'))

def callback2():
    """an ajax callback that returns a <ul> of links to wiki pages"""
    for meeting in db.Meetings:
        for attendee in meeting.attendees.split(','):
            if attendee == auth.user.Name:
                selected += meeting
    selected += db(db.auth.user.Name==db.Meetings.minutetaker).select()
    query = selected.title.contains(request.vars.keyword) or selected.tags.contains(request.vars.keyword)
    pages = db(query).select(orderby=~db.Meetings.id)
    qages = db(page.organiser==db.Organisation.title).select(db.Organisation.id,orderby=~page.id)
    links = [(A(p.title,_href=URL('show',args=[p.id,'Meeting'])),XML(' by<BR/>'),A(p.organiser,_href=URL('show',args=[q.id,'Organisation'])),XML(' on<BR/>'),A(p.dt),XML('Tags:<BR/>'),A(p.tags)) for p,q in pages,qages]
    return DIV(*links)


def templates():
    form = SQLFORM(db.Meetings)
    return dict(form=form)

def formpage():
    form = SQLFORM(db.Meetings)
    if form.process().accepted:
        db.Meetings.templateid[-1] = request.args[0]
        redirect(URL('show',args=[db.Meetings.id[-1],'Meeting']))
    return dict(form=form)
