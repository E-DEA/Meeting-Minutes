# -*- coding: utf-8 -*-
db.define_table('org',
                Field('id',writable=False,requires=IS_NOT_EMPTY()),
                Field('name',requires=IS_NOT_EMPTY()),
                Field('meetings','text',default=request.post_vars.title,requires=IS_NOT_EMPTY()),
                Field('employees','text',requires=IS_NOT_EMPTY()),
                Field('admin_id',requires=IS_NOT_EMPTY())),
