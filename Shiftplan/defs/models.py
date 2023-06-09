from django.db import models
from django.contrib.auth.models import Group, User

# class ShiftplanGroup(models.Model):
#     group = OneToOneField(Group, on_delete=models.CASCADE)
#     shiftplan = OneToOneField()

#     def __str__(self):
#         s = f"Shiftplan Group: {self.group}"
#         return s
class ShiftplanCrew(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through='ShiftplanCrewMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # print(self.shiftplan)
        # self.name = self.shiftplan.name
        super().save(*args, **kwargs)

class ShiftplanCrewMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crew = models.ForeignKey(ShiftplanCrew, on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}, {self.crew}"

class Shiftplan(models.Model):
    name = models.CharField('shiftplan_name', max_length=200, unique=True, blank=False, default="")
    time_format = models.CharField("time_format", max_length=50, default="hourly")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    crew = models.OneToOneField(ShiftplanCrew, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.crew = ShiftplanCrew.objects.create(name=self.name)
        self.crew = ShiftplanCrew.objects.get(name=self.name)


        if self.pk is None:  # create
            self.group = Group.objects.create(name = self.name+"_SP")
        self.group = Group.objects.get(name=self.name+"_SP")
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.name



# class SubCrew(models.Model):
#     name = models.CharField('crew_name', max_length=200, unique=True, blank=False, default="")
#     shiftplan = models.ForeignKey(Shiftplan, on_delete=models.CASCADE)
#     members = models.ManyToManyField(ShiftplanCrewMember)

#     def __str__(self):
#         return self.name 

#     def get_members(self):
#         return self.shiftplan.crew.members.objects.all()#(subcrewmember__crew=self)

    


class TimeInterval(models.Model):
    shiftplan = models.ForeignKey(Shiftplan, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return "{} - {}".format(self.start_date, self.end_date)

    def as_dict(self):
        return {'start_date': self.start_date, 'end_date': self.end_date}
# class Grades(models.Model):
#     shiftplan = models.ForeignKey(Shiftplan, on_delete=models.CASCADE)
#     grade_range = models.PositiveIntegerField(default=5)
#     name = models.CharField('grade_name', max_length=200, unique=True, blank=False, default="")
#
#     def __str__(self):
#         return self.name
# class Subgroup(models.Model):
#     shiftplan = models.ForeignKey(Shiftplan, on_delete=models.CASCADE)
#     name = models.CharField('subgroup name', max_length=200)
#
#     def __str__(self):
#         return self.name
#
#
# class Day(models.Model):
#     shiftplan = models.ForeignKey(Shiftplan, on_delete=models.CASCADE)
#     name = models.CharField('day name', max_length=200)
#     date = models.DateField('date')
#
#     def __str__(self):
#         return str(self.date)

class Jobtype(models.Model):
    shiftplan = models.ForeignKey(Shiftplan, on_delete=models.CASCADE)
    name = models.CharField('jobtype name', max_length=200)
    # subgroup = models.ForeignKey(Subgroup, on_delete=models.CASCADE)
    description = models.TextField('description', default='')  # former "competences"
    # restricted = models.BooleanField() # True if jt is restricted to certain group of users
    # user_group = models.ManyToManyField(User)
    default_rating = models.IntegerField(default=3)
    restricted_to_group = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    # subcrew = models.ForeignKey(Subcrew, on_delete=models.CASCADE, blank=True, null=True)
    

    def save(self, *args, **kwargs):
        # if self.pk is None and self.group is None:
        #     self.group = self.shiftplan.group
        # elif not self.group is None:
        #     self.group = self.group + "_" + self.shiftplan.group

        super().save(*args, **kwargs)  # Call the "real" save() method.


    def __str__(self):
        return self.name

    def as_dict(self):
        return {'name': self.name, 'description': self.description}

# class OldJob(models.Model):
#     jobtype = models.ForeignKey(Jobtype, on_delete=models.CASCADE)
#     begin = models.DateTimeField('job begin')
#     end = models.DateTimeField('job end')
#     rating = models.IntegerField('rating')
#     # during
#     '''Default time formats: ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
#  '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
#  '%Y-%m-%d',             # '2006-10-25'
#  '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
#  '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
#  '%m/%d/%Y',             # '10/25/2006'
#  '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
#  '%m/%d/%y %H:%M',       # '10/25/06 14:30'
#  '%m/%d/%y']             # '10/25/06'
#  '''

class Job(models.Model):
    jobtype = models.ForeignKey(Jobtype, on_delete=models.CASCADE)
    begin_date = models.DateField('job begin date')
    end_date = models.DateField('job end date')
    begin_time = models.TimeField('job begin time')
    end_time = models.TimeField('job end time')
    rating = models.IntegerField('rating', null=True, blank=True)
    # during
    '''Default time formats: ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
 '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
 '%Y-%m-%d',             # '2006-10-25'
 '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
 '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
 '%m/%d/%Y',             # '10/25/2006'
 '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
 '%m/%d/%y %H:%M',       # '10/25/06 14:30'
 '%m/%d/%y']             # '10/25/06'
 '''
    def save(self, *args, **kwargs):
        if self.rating is None:
            self.rating = self.jobtype.default_rating
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return "{jt_name} begin: {b}, {bt} end: {e}, {et}".format(jt_name=self.jobtype.name, b=self.begin_date, e=self.end_date, bt=self.begin_time, et=self.end_time)

    def as_dict(self):
        return {'begin_date': self.begin_date, 'end_date': self.end_date, "begin_time": self.begin_time, "end_time": self.end_time}
#
#
#
# CREATE TABLE Users (
#     id           INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#     fullname_id  INT                NOT NULL UNIQUE,
#     pw           VARCHAR(255)       NOT NULL,
#     nickname     VARCHAR(255)       NOT NULL UNIQUE,
#     email        VARCHAR(255)       NULL,
#     bias         INT                NOT NULL DEFAULT 0,
#     break        INT                NOT NULL DEFAULT 4
# );
#
# CREATE TABLE Names (
#   id         INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#   surname    VARCHAR(255)     NOT NULL,
#   famname    VARCHAR(255)     NOT NULL,
#   registered BOOLEAN          NULL DEFAULT 0,
#   helper     BOOLEAN          NOT NULL DEFAULT 0
# );
#
# CREATE TABLE Helpers (
#   id           INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#   fullname_id  INT                NOT NULL UNIQUE,
#   pw           VARCHAR(255)       NOT NULL,
#   nickname     VARCHAR(255)       NOT NULL UNIQUE,
#   email        VARCHAR(255)       NULL,
#   ticketnumber INT                NULL UNIQUE,
#   workload     INT                NOT NULL DEFAULT 4,
#   break        INT                NOT NULL DEFAULT 4
# );
