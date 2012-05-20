from django import template
from django.utils.html import escapejs
import settings

register = template.Library()

@register.tag('poll_script')
def do_render_poll(parser, tokens):
    try:
        tag_name, poll, domElem = tokens.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % tokens.contents.split()[0])
    return PollNode(poll, domElem)


html="""    <style type="text/css">
        %(domElem)s {
            width: 500px;
            height: 300px;
        }
    </style>
    <script type="text/javascript" src="%(static)sgraphing/raphael-min.js"></script>
    <script type="text/javascript" src="%(static)sgraphing/fancygraphs.js"></script>
    <script type="text/javascript">
        $(document).ready(function(){
            var data = [%(data)s];
            var choiceIds = [%(choiceIds)s];
            graph($('%(domElem)s').get(0), data, "%(voteURL)s", choiceIds, '%(csrf)s', {});
        });
    </script>"""

class PollNode(template.Node):

    def __init__(self, poll, domElem):
        self.poll = template.Variable(poll)
        self.domElem = domElem

    def render(self, context):
        try:
            poll = self.poll.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        data = ','.join([ "['%s',%d]" % (escapejs(str(choice)), votes) for (choice, votes) in poll.results()])
        choiceIds = ','.join([ str(c.id) for c in poll.choice_set.all() ])
        voteURL = poll.get_vote_url()
        csrf = context.get('csrf_token', None)

        static = settings.STATIC_URL
        return html % {"static":static, "data":data, "choiceIds":choiceIds, "voteURL":voteURL, "csrf":csrf, "domElem":self.domElem}



