import Private
from Private import g
from github import Github

# set up the static variables
# None

class Repos:
    @staticmethod
    def GetRepoByName(Owner, RepoName):
        repo = g.get_repo("PyGithub/PyGithub")
        repo.name
    
    @staticmethod
    def Setup():
        Private.AuthUser()

    @staticmethod
    def UserRepos():
        global user
        for repo in g.getuser().getrepos():
            print(repo.name)
    
    @staticmethod
    def GetStars(Owner, RepoName):
        RepoToGetStars = g.get_repo(f"{Owner}/{RepoName}")
        RepoToGetStars.stargazers_count

    @staticmethod
    def GetTopics(Owner, RepoName):
        RepoToGetTopics = g.get_repo(f"{Owner}/{RepoName}")
        RepoToGetTopics.get_topics()
    
    @staticmethod
    def GetIssues(Owner, RepoName):
        RepoToGetIssues = g.get_repo(f"{Owner}/{RepoName}")
        open_issues = RepoToGetIssues.get_issues(state='open')
        for issue in open_issues:
            print(issue)
    
    @staticmethod
    def GetAlerts(Owner, RepoName):
        RepoToGetAlerts = g.get_repo(f"{Owner}/{RepoName}")
        codescan_alerts = RepoToGetAlerts.get_codescan_alerts()
        for alert in codescan_alerts:
            print(alert.number, alert.created_at, alert.dismissed_at)
            print("  ", alert.tool.name, alert.tool.version, alert.tool.guid)
            print("  ", alert.rule.name, alert.rule.security_severity_level, alert.rule.severity)
            print("    ", alert.rule.description)
            print("  ", alert.most_recent_instance.ref, alert.most_recent_instance.state)
            print("    ", alert.most_recent_instance.location)
            print("    ", alert.most_recent_instance.message['text'])

    @staticmethod
    def GetLabels(Owner, RepoName):
        RepoToGetLabels = g.get_repo(f"{Owner}/{RepoName}")
        labels = RepoToGetLabels.get_labels()
        for label in labels:
            print(label)

    @staticmethod
    def GetRootContent(Owner, RepoName):
        RepoToGetRootContent = g.get_repo(f"{Owner}/{RepoName}")
        contents = RepoToGetRootContent.get_contents("")
        for content_file in contents:
            print(content_file)
    
    @staticmethod
    def GetRepoContent(Owner, RepoName):
        RepoToGetContent = g.get_repo(f"{Owner}/{RepoName}")
        contents = RepoToGetContent.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":

                contents.extend(RepoToGetContent.get_contents(file_content.path))
            else:
                print(file_content)
    
    @staticmethod
    def GetFile(Owner, RepoName, FileName):
        RepoToGetFile = g.get_repo(f"{Owner}/{RepoName}")
        contents = RepoToGetFile.get_contents(FileName)
        print(contents)
    
    @staticmethod
    def NewFile(Owner, RepoName, FileName, CommitMessage, Contents, Branch):
        RepoToMakeFile = g.get_repo(f"{Owner}/{RepoName}")
        RepoToMakeFile.create_file(FileName, CommitMessage, Contents, branch=Branch)
    
    @staticmethod
    def DeleteFile(Owner, RepoName):
        RepoToDelFile = g.get_repo(f"{Owner}/{RepoName}")
        contents = RepoToDelFile.get_contents("test.txt", ref="test")
        RepoToDelFile.delete_file(contents.path, "remove test", contents.sha, branch="test")

    @staticmethod
    def TopTenReffers(Owner, RepoName):
        RepoToGetReffers = g.get_repo(f"{Owner}/{RepoName}")
        contents = RepoToGetReffers.get_top_referrers()
        print(contents)

    @staticmethod
    def TopContent(Owner, RepoName):
        RepoToGetTopContent = g.get_repo(f"{Owner}/{RepoName}")
        contents = RepoToGetTopContent.get_top_paths()
        print(contents)

    @staticmethod
    def GetClones(Owner, RepoName):
        RepoToGetClones = g.get_repo(f"{Owner}/{RepoName}")
        contents = RepoToGetClones.get_clones_traffic()
        contents = RepoToGetClones.get_clones_traffic(per="week")
        print(contents)

    @staticmethod
    def GetViews(Owner, RepoName):
        RepoToGetViews = g.get_repo(f"{Owner}/{RepoName}")
        contents = RepoToGetViews.get_views_traffic()
        contents = RepoToGetViews.get_views_traffic(per="week")
        print(contents)

    @staticmethod
    def MarkNotifsRead(Owner, RepoName):
        RepoToMarkNotifsRead = g.get_repo(f"{Owner}/{RepoName}")
        RepoToMarkNotifsRead.mark_notifications_as_read()

class Branches:
    @staticmethod
    def GetBranches(Owner, RepoName):
        RepoToGetBranches = g.get_repo(f"{Owner}/{RepoName}")
        list(RepoToGetBranches.get_branches())

    @staticmethod
    def GetHeadCommit(Owner, RepoName, Branch):
        RepoToGetBranchHeadCommit = g.get_repo(f"{Owner}/{RepoName}").get_branch(Branch)
        RepoToGetBranchHeadCommit.commit

    @staticmethod
    def GetProtectionStatus(Owner, RepoName, Branch):
        RepoToGetBranchProtectionStatus = g.get_repo(f"{Owner}/{RepoName}").get_branch(Branch)
        RepoToGetBranchProtectionStatus.protected

    @staticmethod
    def GetRequiredStatus(Owner, RepoName, Branch):
        RepoToGetRequiredStatus = g.get_repo(f"{Owner}/{RepoName}").get_branch(Branch)
        RepoToGetRequiredStatus.get_required_status_checks()

class Miscellaneous:
    @staticmethod
    def GetCurrentUser():
        user = g.get_user()
        user.login

    @staticmethod
    def GetUserByName(Name):
        user = g.get_user(Name)
        user.name

    @staticmethod
    def GetOrgByName(Org):
        org = g.get_organization(Org)
        org.login

    @staticmethod
    def GECL():
        enterprise = g.get_enterprise_consumed_licenses("PyGithub")
        enterprise_consumed_licenses = enterprise.get_enterprise_consumed_licenses()
        enterprise_consumed_licenses.total_seats_consumed

    @staticmethod
    def WhatsGECL():
        print("GECL stands for: Get Enterprise consumed Licenses by Name")

    @staticmethod
    def SearchRepoByLang():
        repositories = g.search_repositories(query='language:python')
        for repo in repositories:
           print(repo)

class commit:
    @staticmethod
    def GetCommitDate(Commit)
        commit = repo.get_commit(sha=sha)
        print(commit.commit.author.date)

class PR:
    @staticmethod
    def NewPr(Owner, RepoName, Branch, Title, Body):
        RepoToMakePr = g.get_repo(f"{Owner}/{RepoName}")
        RepoToMakePr.create_pull(base=Branch, head="develop", title=Title, body=Body)
    
    @staticmethod
    def GetPrByNum(Owner, RepoName, PrNum):
        RepoToGetPr = g.get_repo(f"{Owner}/{RepoName}")
        RepoToGetPr.get_pull(PrNum)

    @staticmethod
    def GetPrByQuery(Owner, RepoName, State, Topic):
        if state not in ["Open","Closed"]:
            raise ValueError("State must be 'Open' or 'Closed'")
        else:
            RepoToGetPr = g.get_repo(f"{Owner}/{ReponName}")
            pulls = RepoToGetPr.get_pulls(state=State, sort=Topic, base='master')
            for pr in pulls:
               print(pr.number)

    @staticmethod
    def comment(Owner, RepoName, Content):
        RepoToComment = g.get_repo(f"{Owner}/{RepoName}")
        pr = repo.get_pull(2390)
        pr.create_comment(Content)

class issues:
    @staticmethod
    def GetIssue(Owner, RepoName, IssueNum):
        RepoToGetIssue = g.get_repo(f"{Owner}/{RepoName}")
        RepoToGetIssue.get_issue(number=IssueNum)

    @staticmethod
    def CommentOnIssue(Owner, RepoName, IssueNum, Comment):
        RepoToCommentIssue = g.get_repo(f"{Owner}/{RepoName}")
        issue = RepoToCommentIssue.get_issue(number=IssueNum)
        issue.create_comment(Comment)

    @staticmethod
    def NewIssue(Owner, RepoName, Title, Body):
        RepoToGet = g.get_repo(f"{Owner}/{RepoName}")
        repo.create_issue(title=Title, body=Body)

    @staticmethod
    def CloseIssues(Owner, RepoName):
        RepoToCloseIssues = g.get_repo(f"{Owner}/{RepoName}")
        open_issues = RepoToCloseIssues.get_issues(state='open')
        for issue in open_issues:
            issue.edit(state='closed')
    
class milestone:
    @staticmethod
    def GetMsList(Owner, RepoName, State):
        if state not in ["Open","Closed"]:
            raise ValueError("State must be 'Open' or 'Closed'")
        else:
            RepoToGetLs = g.get_repo(f'{Owner}/{RepoName}')
            open_milestones = RepoToGetLs.get_milestones(state=State)
            for milestone in open_milestones:
               print(milestone)

    @staticmethod
    def GetMs(Owner, RepoName, MsNum):
        RepoToGetMs = g.get_repo(f'{Owner}/{RepoName}')
        RepoToGetMs.get_milestone(number=MsNum)

    @staticmethod
    def MakeMs(Owner, RepoName, Title, Desc):
        RepoToMakeMs = g.get_repo(f'{Owner}/{RepoName}')
        RepoToMakeMs.create_milestone(title=Title, description=Desc)        
