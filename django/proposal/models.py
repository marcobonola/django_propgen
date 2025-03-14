from django.db import models

from markdownx.models import MarkdownxField
from adminsortable.fields import SortableForeignKey

from collections import defaultdict
from decimal import Decimal

import reversion 

import reorderhelper.models 
import revisionhelper.views


@reversion.register()
class SomeModel(reorderhelper.models.ReorderableMixin,
                    models.Model):
    model_name = "Some model"
    
    title = models.CharField(verbose_name="Descriptive title",
                             blank=True,
                             max_length=80)


    included = models.BooleanField(
        verbose_name="Include this block in ouput"
    )

    def __str__(self):
        return "SomeModel: " + self.title  + super().__str__()
    


@reversion.register()
class Textblock(reorderhelper.models.ReorderableMixin,
    models.Model):

    name = models.CharField(
        verbose_name="Short name of the textblock",
        help_text="This name is used to refer to the textblock in templates",
        max_length=64,
    )

    description = models.TextField(
        verbose_name="Brief description",
        help_text="Provide a brief description of this block;"
        "leave empty if clear; does not end up in output"
    )

    filename = models.CharField(
        verbose_name="Filename for the content of the textblock",
        help_text="Provide a filename if you want the content of "
        "this textblock to written to a markdown file. If empty, "
        "no file is produced automatically; content has to be used "
        "in a template explicitly, then.",
        max_length=64,
        blank=True, null=True,
    )

    textblock = MarkdownxField(
        verbose_name="Actual text",
        help_text="Actual text for this block, in Markdown format"
    )

    def __str__(self):
        return "{} {}".format(
            self.name,
            ("({})".format(self.description[0:50])
             if self.description else ""),
        )


@reversion.register()
class Bibliography(reorderhelper.models.ReorderableMixin,
                  models.Model):
    filename = models.CharField(
        verbose_name="Name of the bibliography file, including extension",
        help_text=("Extension of the filename will be used to determine how "
                  "to process this file."),
        max_length=64,
    )

    bibliography = models.TextField(
        verbose_name="Biboliographic information",
        help_text=("Enter the actual bibliographic information, "
                   "depending on the format you are using. ")
    )

    def __str__(self):
        return self.filename

@reversion.register()
class Partnertype(reorderhelper.models.ReorderableMixin,
                  models.Model):
    shortname = models.CharField(max_length=20,
                            help_text="Short form of partner types")
    description = models.CharField(max_length=128)

    def __str__(self):
        return "{}: {}".format(self.shortname, self.description)

@reversion.register()
class Partner(reorderhelper.models.ReorderableMixin,
                  models.Model):


    partnername = models.CharField(max_length=255)
    shortname = models.CharField(max_length=80)

    partnertype = models.ForeignKey(Partnertype,
                             blank=True, null=True)

    pic = models.CharField(max_length=16,
                           verbose_name="PIC",
                           help_text="Participant Identification Code",
                           default="")

    description = MarkdownxField(
        verbose_name="Partner description in general",
        help_text="General description text, will appear before the subsections defined below. "
        "Typically empty if you fill in the following sections.",
        blank=True,
    )
    organization = MarkdownxField(
        verbose_name="Organization",
        help_text="a description of the legal entity and its main tasks, "
                  "with an explanation of how its profile matches the tasks in the proposal",
        blank=True,
    )
    individuals = MarkdownxField(
        verbose_name="Individual researchers",
        help_text="CV or description of key personnel",
        blank=True,
    )
    partnerpublications = MarkdownxField(
        verbose_name="Relevant publications, products and/or services",
        help_text="Up to 5 relevant publications, products, services",
        blank=True,
    )
    partnerprojects = MarkdownxField(
        verbose_name="Previous projects",
        help_text="Up to 5 previous project or activities, relevant to the proposal",
        blank=True,
    )
    infrastructure = MarkdownxField(
        verbose_name="Significant infrastructure",
        help_text="Significant infrastructure and/or major technical equipment, "
        "relevant to the project",
        blank=True,
    )


    country = models.CharField(max_length=3)

    #############################
    # Budget-related information

    PMcost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Person month cost",
        help_text="This relates to the Direct Personnel Cost (Col. A) via the number of personmonths",
        default=Decimal('0'),
    )

    reimbursement_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Reimbursement rate",
        help_text="Make sure the reimbursement rate is consistent with the partner type",
        default=Decimal('100'),
    )

    _other_direct_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Other direct cost",
        help_text="Corresponds to Col. B. If negative, the value is computed from other fields!",
        default=Decimal('-1'),
    )

    other_direct_cost_explanation = MarkdownxField(
        verbose_name="Explanation for other direct cost",
        help_text="Provide explanation for other direct cost if they exceed 15% of the personnel cost (as per guidelines).",
        blank=True,
    )

    subcontract_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Subcontractig cost",
        help_text="Total cost of all subcontracting done by this partner",
        default=Decimal('0'),
    )

    subcontract_cost_explanation = MarkdownxField(
        verbose_name="Explanation for subcontracts",
        help_text="Usually, explanation for subcontracting is necessary",
        blank=True,
    )

    finanical_support_3rd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Financial support for 3rd parties",
        default=Decimal('0'),
    )

    finanical_support_3rd_explanation = MarkdownxField(
        verbose_name="Explanation of financial support to 3rd parties",
        help_text="Provide explanation",
        blank = True,
    )

    inkind_contributions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="In-kind contributions",
        default = Decimal('0'),
    )

    inkind_contributions_explanations = MarkdownxField(
        verbose_name="Explanation of in-kind contributions",
        blank=True,
    )

    special_uni_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Special unit cost",
        default = Decimal('0'),
    )

    special_uni_cost_explanation = MarkdownxField(
        verbose_name="Explanation of special unit cost",
        blank=True,
    )

    _requested_contribution = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Requested contribution",
        help_text="Default negative value means requested contribution equals maximum contribution."
                  "Only fill in this field if you want to request less money than the maximum "
                  "allows you to do. This is usually not recommended.",
        default = Decimal('-1'),
    )

    @property
    def other_direct_cost(self):
        if self._other_direct_cost < 0:
            return self.personmonths*self.PMcost * Decimal('0.15')
        else:
            return self._other_direct_cost

    @property
    def personmonths(self):
        ae = allEfforts().data
        return sum([x["effort"] for x in ae if x['partner'] == self])

    @property
    def personnel_cost(self):
        return self.PMcost * self.personmonths

    @property
    def indirect_cost(self):

        return (self.personmonths*self.PMcost +
                     self.other_direct_cost +
                     self.inkind_contributions) * Decimal('0.25')

    @property
    def total_cost(self):
        return (self.personmonths*self.PMcost +
                self.other_direct_cost +
                self.subcontract_cost +
                self.finanical_support_3rd +
                self.indirect_cost +
                self.special_uni_cost
                )

    @property
    def maxcontribution(self):
        return self.reimbursement_rate * self.total_cost

    @property
    def requested_contribution(self):
        if self._requested_contribution < 0:
            r = self.maxcontribution
            return r
        else:
            return self._requested_contribution

    @property
    def number(self):
        return 99


    @property
    def budget_explanations(self):
        return (len(self.other_direct_cost_explanation) > 0 or
                len(self.subcontract_cost_explanation) > 0 or
                len(self.finanical_support_3rd_explanation) > 0  or
                len(self.inkind_contributions_explanations) > 0 or
                len(self.special_uni_cost_explanation) > 0
                )


    dictkey = "shortname"

    def __str__(self):
        return "{} ({})".format(self.partnername ,
                                self.shortname)

@reversion.register()
class Workpackage(reorderhelper.models.ReorderableMixin,
                  models.Model):
    title = models.CharField(max_length=255)
    tag = models.CharField(max_length=20)
    objectives = MarkdownxField()
    description = MarkdownxField()

    type = models.CharField(
        verbose_name="WP Type (RTD, MGMT, ...)",
        help_text="Type of the WP, according to predefined EU list",
        max_length=10,
        default="RTD",
    )

    lead = models.ForeignKey(Partner)

    @property
    def startmonth(self):
        try:
            r = min([x.start for x in self.Task_set])
        except Exception:
            r = 1

        return r

    @property
    def endmonth(self):

        try:
            r = max([x.end for x in self.Task_set])
        except Exception:
            r = Project.objects.first().duration

        return r

    @property
    def duration(self):
        return (self.endmonth -
                self.startmonth + 1)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']



@reversion.register()
class Task(reorderhelper.models.ReorderableMixin,
                  models.Model):
    title = models.CharField(max_length=255)
    tag = models.CharField(max_length=20)

    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()

    objectives = MarkdownxField()
    description = MarkdownxField()

    wp = SortableForeignKey(Workpackage)
    lead = models.ForeignKey(Partner)

    def __str__(self):
        return self.title

    def interval(self):
        return [(self.start, self.end), ]

    def contributors(self):
        return set([x.partner.shortname for x in self.taskpartnerpm_set.all()])

    class Meta:
        ordering = ['order']


class ProducableTypes(models.Model):
    short = models.CharField(max_length=10)
    long = models.CharField(max_length=200,
                            blank=True, null=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return "{} ({})".format(self.long, self.short)


class DisseminationTypes(models.Model):
    short = models.CharField(max_length=10)
    long = models.CharField(max_length=200,
                            blank=True, null=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return "{} ({})".format(self.long, self.short)


@reversion.register()
class Deliverable(reorderhelper.models.ReorderableMixin,
                  models.Model):
    title = models.CharField(max_length=255)
    tag = models.CharField(max_length=20)
    description = MarkdownxField()
    due = models.PositiveIntegerField()
    lead = models.ForeignKey(Partner)
    maintask = models.ForeignKey(Task,
                                 blank=True)
    secondarytasks = models.ManyToManyField(
        Task,
        blank=True,
        related_name="deliverable_secondaryTasks")

    type = models.ForeignKey(ProducableTypes)
    dissemination = models.ForeignKey(DisseminationTypes)

    wp = SortableForeignKey(Workpackage)

    def __str__(self):
        return self.title

    @property
    def tasklist(self):
        # print("tasklist")
        l1 = ["\\textbf{{\\ref{{{}}}}}".format(self.maintask.tag)]
        # print(l1)
        l2 = ["\\ref{{{}}}".format(t.tag) for t in self.secondarytasks.all()]
        # print(l2)
        r = ", ".join(l1 + l2)
        # print(r)
        return r

    class Meta:
        ordering = ['order']


@reversion.register()
class Milestone(reorderhelper.models.ReorderableMixin,
                  models.Model):
    title = models.CharField(max_length=255)
    tag = models.CharField(max_length=20)

    description = MarkdownxField()
    due = models.PositiveIntegerField()
    lead = models.ForeignKey(Partner)
    maintask = models.ForeignKey(Task, blank=True)
    secondarytasks = models.ManyToManyField(
        Task,
        related_name="milestone_secondaryTasks")

    verification = MarkdownxField()

    wp = SortableForeignKey(Workpackage)

    @property
    def tasklist(self):
        # print("tasklist")
        l1 = ["\\textbf{{\\ref{{{}}}}}".format(self.maintask.tag)]
        # print(l1)
        l2 = ["\\ref{{{}}}".format(t.tag) for t in self.secondarytasks.all()]
        # print(l2)
        r = ", ".join(l1 + l2)
        # print(r)
        return r


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


@reversion.register()
class TaskPartnerPM(models.Model):
    partner = models.ForeignKey(Partner)
    task = models.ForeignKey(Task)

    effort = models.DecimalField(max_digits=6,
                                 decimal_places=2)


    def __str__(self):
        return "{} for task {}: {}".format(
            self.partner,
            self.task,
            self.effort
        )

@reversion.register()
class DeliverablePartnerTaskPM(models.Model):
    partner = models.ForeignKey(Partner)
    deliverable = models.ForeignKey(Deliverable)
    task = models.ForeignKey(Task)

    effort = models.DecimalField(max_digits=6,
                                 decimal_places=2)

    def __str__(self):
        return "{} @ del. {} for task {}: {}".format(
            self.partner,
            self.deliverable,
            self.task,
            self.effort
        )

    class Meta:
        verbose_name = "PM per partner, per task, per deliverable"

@reversion.register()
class MilestonePartnerTaskPM(models.Model):
    partner = models.ForeignKey(Partner)
    milestone = models.ForeignKey(Milestone)
    task = models.ForeignKey(Task)

    effort = models.DecimalField(max_digits=6,
                                 decimal_places=2)


    def __str__(self):
        return "{} @ MS {} for task {}: {}".format(
            self.partner,
            self.milestone,
            self.task,
            self.effort
        )


@reversion.register()
class Project(
    models.Model):

    title = models.CharField(verbose_name="Project title",
                             max_length=512,
                             )

    shortname = models.CharField(
        verbose_name="Project short name or acronym",
        max_length=128)

    lead = models.ForeignKey(
        Partner,
        verbose_name="Project coordinator (partner)",
        blank=True, null=True,
        )

    duration = models.PositiveIntegerField(
        verbose_name="Project duration (in months)")

    projecttype = models.CharField(
        verbose_name="Project type",
        help_text="Project type like STREP, IA, IP, ...",
        max_length=64,
        blank = True, null = True,
    )

    callid = models.CharField(
        verbose_name="Call identifier",
        help_text="EU call ID like ICT FP7-ICT-2012-8 ",
        max_length=30,
        blank=True, null=True,
    )

    callobjectives = models.CharField(
        verbose_name="Call objectives",
        help_text="Use identifiers or short names from call",
        max_length=128,
        blank=True, null=True,
    )

    coordinatorName = models.CharField(
        verbose_name="Name of coordinating person",
        max_length=128,
        blank=True, null=True,
    )

    coordinatorEmail = models.EmailField(
        verbose_name="Email of the coordinating person",
        blank=True, null=True,
    )

    coordinatorPhone = models.CharField(
        verbose_name="Phone/FAX number of coordinator",
        max_length=128,
        blank=True, null=True,
    )

    def __str__(self):
        return self.shortname + ": " + self.title[:50]


@reversion.register()
class Setting(models.Model):
    group = models.CharField(verbose_name="Settings group",
                             max_length=64)

    name = models.CharField(verbose_name="Settings name",
                            max_length=128)

    value = models.CharField(verbose_name="Settings value",
                             max_length=256)

    description = models.TextField(
        verbose_name="Description of this setting",
        help_text="Explain what this setting does, where it is used.",
        blank=True,
    )
    class Meta:
        ordering = ['group', 'name']
    def __str__(self):
        return "{}.{} = {}".format(self.group, self.name, self.value)

    def get_default(group="", name=""):
        try:
            s = Setting.objects.filter(group__exact=group,
                                       name__startswith=name).first()
            return s.value
        except:
            from django_propgen.settings import default_settings
            # print(default_settings[group])
            return default_settings[group][name]

        return None


@reversion.register()
class Template(models.Model):
    name = models.CharField(
        verbose_name="Name of the produced file",
        help_text="Include extensions like .tex or .md",
        max_length=64)

    description = models.TextField(
        verbose_name="Description",
        help_text="Provide a brief description of what this template does"
    )

    template = models.TextField(
        verbose_name="Actual template text",
        help_text="Use Jinja2-style templates",
        )

    PRODUCE_LATEX = "LA"
    PRODUCE_MARKDOWN = "MD"

    PRODUCTION_TYPES = (
        (PRODUCE_LATEX, "Latex",),
        (PRODUCE_MARKDOWN, "Markdown",),
    )

    startpoint = models.BooleanField(
        verbose_name="Start point",
        help_text="Should this template be offered as a possible "
        "starting point from which to produce PDFs?",
        default=False,

    )

    def __str__(self):
        return (self.name
                if not self.description
                else "{} ({})".format(
                    self.name, self.description[0:50]))


############
class allEfforts():
    """A class to collect all the different types of efforts
    in a convenient list of dictionaries. Intended for easy access in
    templates."""

    def __init__(self):
        self.data = []

        for partner in Partner.objects.all():
            for task in TaskPartnerPM.objects.filter(partner=partner):
                eff = {'partner': partner,
                       'task': task.task,
                       'wp': task.task.wp,
                       'effort': task.effort}

                for deliverable in DeliverablePartnerTaskPM.objects.filter(
                    partner=partner, task=task.task,
                    ):
                    eff['effort'] += deliverable.effort

                for milestone in MilestonePartnerTaskPM.objects.filter(
                    partner=partner, task=task.task,
                    ):
                    eff['effort'] += milestone.effort

                self.data.append(eff)


# Make sure that the Reversions ViewSet can find all the relevant models:
import inspect
import sys
revisionhelper.views.ReversionsViewSet.model_list.update(
    dict(inspect.getmembers(sys.modules[__name__], inspect.isclass)))
