def owner_name_of(reponame):
    '''
    owner, name = owner_name_of(repository_name)
    '''
    owner,_,name = reponame.partition('/')
    return owner, name
