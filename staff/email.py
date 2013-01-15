from datetime import datetime, time, date, timedelta
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from models import Member, DailyLog
import settings, mailchimp

def send_introduction(user):
	site = Site.objects.get_current()
	subject = "%s: Introduction to Nadine" % (site.name)
	message = render_to_string('email/introduction.txt', {'user':user, 'site':site})
	send_mail(subject, message, settings.EMAIL_ADDRESS, [user.email], fail_silently=True)
	subscribe_to_newsletter(user.email)

def subscribe_to_newsletter(email):
	if settings.MAILCHIMP_NEWSLETTER_KEY:
		try:
			newsletter = mailchimp.utils.get_connection().get_list_by_id(settings.MAILCHIMP_NEWSLETTER_KEY)
			newsletter.subscribe(email, {'EMAIL':email})
		except:
			pass

def send_new_membership(user):
	site = Site.objects.get_current()
	membership = user.profile.last_membership()
	subject = "%s: New %s Membership" % (site.name, membership.membership_plan.name)
	message = render_to_string('email/new_membership.txt', {'user':user, 'membership':membership, 'site':site})
	send_mail(subject, message, settings.EMAIL_ADDRESS, [user.email], fail_silently=False)	

def send_first_day_checkins():
	now = datetime.now()
	midnight = now - timedelta(seconds=now.hour*60*60 + now.minute*60 + now.second)
	free_trials = DailyLog.objects.filter(visit_date__range=(midnight, now), payment='Trial')
	for l in free_trials:
		send_first_day_checkin(l.member.user)

def send_first_day_checkin(user):
	site = Site.objects.get_current()
	subject = "%s: How was your first day?" % (site.name)
	message = render_to_string('email/first_day.txt', {'user':user, 'site':site})
	send_mail(subject, message, settings.EMAIL_ADDRESS, [user.email], fail_silently=False)

def send_invalid_billing(user):
	site = Site.objects.get_current()
	subject = "%s: Billing Problem" % (site.name)
	message = render_to_string('email/invalid_billing.txt', {'user':user, 'site':site})
	send_mail(subject, message, settings.EMAIL_ADDRESS, [user.email], fail_silently=False)	

def announce_new_member(member):
	subject = "New User - %s" % (member)
	message = "Team,\r\n\r\n \t%s just signed in for the first time!\r\n\r\n - Nadine" % (member)
	send_mail(subject, message, settings.EMAIL_ADDRESS, [settings.TEAM_EMAIL_ADDRESS], fail_silently=True)

def announce_need_photo(member):
	subject = "Photo Opportunity - %s" % (member)
	message = "Team,\r\n\r\n \t%s just signed in and we don't have a photo of them yet.\r\n\r\n - Nadine" % (member)
	send_mail(subject, message, settings.EMAIL_ADDRESS, [settings.TEAM_EMAIL_ADDRESS], fail_silently=True)