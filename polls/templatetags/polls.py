from django import template
from django.utils.html import escapejs
import settings

register = template.Library()

poll_html = '''
    <div id="poll_container%(id)d">
        <noscript>
            <img src="%(image_URL)s" />
            <form class="well form-inline" action="%(vote_URL)s" method="post">
                <div style='display:none;'><input type='hidden' id='csrfmiddlewaretoken' name='csrfmiddlewaretoken' value='%(csrf)s'/></div>
                Vote For:
                %(choices)s
            </form>
        </noscript>
        <script type="text/javascript">
            $(document).ready(function(){
                var data = [%(data)s];
                var choiceIds = [%(choiceIds)s];
                graph($('#poll_container%(id)d').get(0), data, "%(vote_URL)s", choiceIds, '%(csrf)s', {});
            });
        </script>
        <style type="text/css">
            #poll_container%(id)d {
                width: 500px;
                height: 300px;
            }
        </style>
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

