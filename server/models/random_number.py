from django.db import models
from django.utils.translation import ugettext_lazy as _
import random

class RandomNumberDraw(models.Model):
    """
    Class that represents a draw with the details to produce random numbers.
    """

    range_min = models.BigIntegerField(_("Range start"), blank=False, null=False, default=0)
    """"Minimun value to be generated. Inclusive."""

    range_max = models.BigIntegerField(_("Range End"), blank=False, null=False)
    """"Maximun value to be generated. Exclusive."""

    number_of_results = models.PositiveIntegerField(_("Number of results"), blank=False, null=False, default=1)
    """Number of Random numbers to generate"""

    allow_repeat = models.BooleanField(_("Allow Repetitions"), blank=False, null=False, default=False)
    """Whether the set of numbers to generate can contain repetitions. Note, if false, max-min > num_res"""


    def is_feasible(self):
        if self.range_max is None:
            return False
        if self.allow_repeat == True:
            return  self.range_min < self.range_max
        else:
            return self.range_max - self.range_min >= self.number_of_results


    def toss(self):
        """Carries out the toss"""
        result = RandomNumberResult()
        result.draw = self
        result.save()

        for i in range(0,self.number_of_results):
            random_value = random.randint(self.range_min, self.range_max)
            number = Number(value = random_value)
            number.result=result
            number.save()



class RandomNumberResult(models.Model):
    """
    Class that represents a result of a RandonNumberDraw
    Note that one draw can generate several results
    """
    class Meta:
        app_label="server"

    draw = models.ForeignKey(RandomNumberDraw, verbose_name=_("Draw"), blank=False, null=False, unique=False, related_name="draw_results")
    """ Stores the draw that generated this result. """

    #number = models.ManyToManyField(Number, verbose_name=_("Number"), blank=False, null=False, unique=False, related_name="result_numbers")



class Number(models.Model):
    """
    Class that store a number as the result (or part of it) of a RandomNumberDraw
    Note that one result may be one or several numbers
    """
    value = models.BigIntegerField(_("Number"), blank=False, null=False)

    result = models.ForeignKey(RandomNumberResult, verbose_name=_("Result"), blank=False, null=False, unique=False, related_name="result_numbers")

    class Meta:
        app_label="server"