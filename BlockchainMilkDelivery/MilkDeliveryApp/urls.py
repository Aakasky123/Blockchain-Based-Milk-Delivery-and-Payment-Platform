from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path("AdminLogin.html", views.AdminLogin, name="AdminLogin"),
	       path("StaffLogin.html", views.StaffLogin, name="StaffLogin"),
	       path("index.html", views.Logout, name="Logout"),
	       path("AddStaff.html", views.AddStaff, name="AddStaff"),
	       path("AdminLoginAction", views.AdminLoginAction, name="AdminLoginAction"),
	       path("AddStaffAction", views.AddStaffAction, name="AddStaffAction"),	
	       path("AddFarmer.html", views.AddFarmer, name="AddFarmer"),
	       path("AddFarmerAction", views.AddFarmerAction, name="AddFarmerAction"),
	       path("ViewFarmer.html", views.ViewFarmer, name="ViewFarmer"),
	       path("ViewStaff.html", views.ViewStaff, name="ViewStaff"),
	       path("AddDelivery.html", views.AddDelivery, name="AddDelivery"),
	       path("AddDeliveryAction", views.AddDeliveryAction, name="AddDeliveryAction"),
	       path("ViewDelivery.html", views.ViewDelivery, name="ViewDelivery"),
	       path("ViewDeliveryAction", views.ViewDeliveryAction, name="ViewDeliveryAction"),
	       path("StaffLoginAction", views.StaffLoginAction, name="StaffLoginAction"),
	       path("FarmerLogin.html", views.FarmerLogin, name="FarmerLogin"),
	       path("FarmerLoginAction", views.FarmerLoginAction, name="FarmerLoginAction"),
	       path("ViewFarmerDelivery", views.ViewFarmerDelivery, name="ViewFarmerDelivery"),
]