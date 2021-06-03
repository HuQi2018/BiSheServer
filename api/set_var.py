# 设置在模板中使用set命令定义变量：
# http://cache.baiducontent.com/c?m=rrtb3uN2RnzgKr563i3L9reJnG9mu2hucEzKWaoyZzttkzkJv-c11qyJlfn2nHajhC9Kq7Ns1j506a2pgFXw-VCIx-btAMV0_z0lcJ4cvP7PEujobJp7rgtrBhVIQ6uZxq-AiNi1hOAJIV7bLkRuck1Sxwv137-J3Yn9-aI_DnfF6GU7UPl5htaY3UNaoN6dQkMPTXH5s-9pDCTcddk0qa&p=882a9644d0dd12a05ab0db391555bb&newp=c272d716d9c111a05bec92371e5e97231610db2151d6d4176b82c825d7331b001c3bbfb423291600d5cf7c6000ab4b58eff132763d0923a3dda5c91d9fb4c57479&s=cfcd208495d565ef&user=baidu&fm=sc&query=django+++template%C0%EF%B6%A8%D2%E5%C4%AC%C8%CF%CA%FD%D7%E9&qid=fa71480c00004f45&p1=3

from django import template

register = template.Library()


class SetVarNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


def set_var(parser, token):
    """
      {% set <var_name> = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")
    return SetVarNode(parts[1], parts[3])


register.tag('set', set_var)
