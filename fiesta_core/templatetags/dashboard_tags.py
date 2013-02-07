from django import template

from fiesta_core.apps.dashboard.nav import get_nodes

register = template.Library()




def dashboard_navigation(parser, token):
    return DashboardNavigationNode()


class DashboardNavigationNode(template.Node):

    def render(self, context):
        user = context['user']
        context['nav_items'] = get_nodes(user)
        return ''


register.tag('dashboard_navigation', dashboard_navigation)
