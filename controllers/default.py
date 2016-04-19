# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


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
    return dict(form=auth())


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

def minutes(): 
    fields = [field for field in db.Meetings]
    inter = fields + [Field('organisations',requires=IS_NOT_EMPTY,label='Organisations')]
    intra = fields + [Field('chair',requires=IS_NOT_EMPTY,label='Chair')]
    pta = fields + [Field('Subject')]
    interform = SQLFORM.factory(*inter,formstyle='bootstrap',table_name='intertable').process()
    return locals()

def search():
    return dict(FORM(INPUT(_id='keyword',_name='keyword',_onkeyup="ajax('callback',['keyword'],'target');")),
                target_div=DIV(_id='target'))
def callback():
    """an ajax callback that returns a <ul> of links to wiki pages"""
    query = db.Meetings.title.contains(request.vars.keyword) or db.Meetings.tags.contains(request.vars.keyword)
    pages = db(query).select(db.Meetings.ALL,orderby=-db.Meetings.id)
    return dict(pages=pages)
    links = [A(p.title, _href=URL('show',args=p.id)) for p in pages]
    return UL(*links)
