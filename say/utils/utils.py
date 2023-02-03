from wagtail.admin.panels import InlinePanel


class FormableInlinePanel(InlinePanel):
    def __init__(self, relation_name, form=None, *args, **kwargs):
        self.form = form
        super(FormableInlinePanel, self).__init__(relation_name, *args, **kwargs)

    def clone_kwargs(self):
        kwargs = super(FormableInlinePanel, self).clone_kwargs()
        kwargs.update(form=self.form)
        return kwargs

    def get_form_options(self):
        form_options = super(FormableInlinePanel, self).get_form_options()
        form_options["formsets"][self.relation_name].update(form=self.form)
        return form_options
