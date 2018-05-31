import urllib
import urllib2
import cookielib
import os
import thread
import commands


def makeCookie(name,value):
    return cookielib.Cookie(
        0,
        name,
        value,
        None,
        False,
        'build2.inse.lucent.com',
        False,
        False,
        '/bugzilla',
        False,
        False,
        None,
        True,
        None,
        None,
        None,
    )
def queryPage(start,end):
    url = urllib.unquote(r'''http://build2.inse.lucent.com/bugzilla/buglist.cgi?bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&email1=&emailtype1=substring&emailassigned_to1=1&email2=&emailtype2=substring&emailreporter2=1&changedin=&chfield=%5BBug+creation%5D&chfieldfrom=%s&chfieldto=%s&chfieldvalue=&telica_subversion=&telica_subversion_type=substring&short_desc=&short_desc_type=substring&long_desc=&long_desc_type=substring&bug_file_loc=&bug_file_loc_type=substring&sqa_identity=&sqa_identity_type=substring&branch=NONE&checkedInAfter=&checkedInBefore=&cmdtype=doit&newqueryname=&order=%22Importance%22&form_name=query''')
    cookie = cookielib.CookieJar()
    #get buglist cookie
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    response = opener.open(url%(start,end))
    #refresh request with columnlist
    cookie.set_cookie(makeCookie('COLUMNLIST','''opendate changeddate severity priority platform owner reporter status resolution compMajID compMinID product telica_version project os target_milestone status_whiteboard escalations customer featureID backport ccb area SQAReview bug_file_loc rca_tea summary summaryfull'''))
    response = opener.open(url%(start,end))
    return response.read()

def subthread(path,buglist,host,user,password,database,table):
    command = "%s/bin/dbimport.sh -f %s -h %s -u %s -p %s -d %s -n %s"%(path,buglist,host,user,password,database,table)
    print command
    ret,output = commands.getstatusoutput(command)
    if ret != 0:
        print output
        return False
    else:
        return True
    

def ImportMain(start, end, path,arg0,arg1,arg2,arg3,arg4):
    filename = path+'/buglists/buglist_'+start+'_'+end+'.html'
    buglist = open(filename,r"w+")
    try:
        buglist.write(queryPage(start,end))
    except IOError as e :
        print e
    buglist.close()
    print "Done for create buglist file"
    try:
        print "starting thread"
        ret = subthread(path,filename,arg0,arg1,arg2,arg3,arg4)
    except:
        print "Error in subthread"
    print ret
    return ret
'''
for i in cookie:
    print '--------------------------'
    print "Version = "+str(i.version)
    print "Name = "+str(i.name)
    print "Value = "+str(i.value)
    print "Port = "+str(i.port)
    print "Path = "+str(i.path)
    print "Secure = "+str(i.secure)
    print "Expires = "+str(i.expires)
    print "Discard = "+str(i.discard)
    print "Comment = "+str(i.comment)
    print "Comment_url = "+str(i.comment_url)
    print "Rfc2109 = "+str(i.rfc2109)
    print "Port_specified = "+str(i.port_specified)
    print "Domain = "+str(i.domain)
    print "Domain_specified = "+str(i.domain_specified)
    print "Domain_initial_dot = "+str(i.domain_initial_dot)
'''

if __name__ == '__main__':
    
    ImportMain(sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])
