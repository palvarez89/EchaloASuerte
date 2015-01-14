from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div, HTML
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

#When a new deck is added, add it also in the dict in card.py
DECKS_CHOICES = (('french', _("French")),
                 ('spanish', _("Spanish")),
                 )

class CardDrawForm(forms.Form):
    number_of_results = forms.IntegerField(label=_("Number of cards to draw"), required=True, initial=1, max_value=20)
    #type_of_deck = forms.CharField(label=_("Type of deck"), required=True, initial="french")
    type_of_deck = forms.ChoiceField(required=True, initial="french", choices=DECKS_CHOICES)

    def __init__(self, *args, **kwargs):
        super(CardDrawForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'form-random_number'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-5'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('card')
        self.helper.layout = Layout(
            Row('number_of_results'),
            Row('type_of_deck'),
            Row(HTML("{% include 'render_errors.html' %}")),
            Div(
               Submit('submit', _("Toss"), css_class='btn btn-primary'),
               css_class='text-center',
            )
        )
