from django import template
from django.utils.html import escapejs
import settings

register = template.Library()

poll_html = '''
    <div id="poll_container%(id)d" style="width: 500px; height: 300px;">
        <noscript>
            <img src="%(image_URL)s" alt="poll rendered here" />
            <form class="well form-inline" action="%(vote_URL)s" method="post">
                Vote For:
                %(choices)s
            </form>
        </noscript>
        <script type="text/javascript">
            data[%(id)d] = [%(data)s];
            choiceIds[%(id)d] = [%(choiceIds)s];
            vote_URLs[%(id)d] =  "%(vote_URL)s";
            csrf = "%(csrf)s";
            $('#poll_container%(id)d').bind('isVisible', graph);
        </script>
    </div>'''

@register.tag('poll')
def do_render_poll(parser, tokens):
    try:
        tag_name, poll = tokens.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly 1 arguement" % tokens.contents.split()[0])
    return PollNode(poll)

class PollNode(template.Node):

    def __init__(self, poll):
        self.poll = template.Variable(poll)

    def render(self, context):
        try:
            poll = self.poll.resolve(context)
        except template.VariableDoesNotExist:
            return '%s does not exist' % str(self.poll)

        #Every poll get an id so that we can apply js/css to it.
        #This is where we can actually store our custom variables...
        #From: http://stackoverflow.com/questions/2566265/is-there-a-django-template-tag-that-lets-me-set-a-context-variable
        POLLCOUNTKEY = "pollcount"
        c = context.dicts[0] 
        pollcount = c[POLLCOUNTKEY] if POLLCOUNTKEY in c else 0
        c[POLLCOUNTKEY] = pollcount + 1

        choices = "\n".join([
            '<input type="submit" value="' + choice.choice + '" name="choice" />'
            for choice in poll.choice_set.all()])

        data = ','.join([ "['%s',%d]" % (escapejs(str(choice)), votes) for (choice, votes) in poll.results()])
        choiceIds = ','.join([ str(c.id) for c in poll.choice_set.all() ])

        return poll_html % {
            "image_URL": poll.get_image_url(),
            "vote_URL": poll.get_vote_url(),
            "choices":choices,
            "csrf": context.get('csrf_token', None),
            "id":pollcount,
            "data":data,
            "choiceIds": choiceIds
        }

