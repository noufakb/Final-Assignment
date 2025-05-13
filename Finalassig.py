#Importing needed libraries for the code such as GUI,datastorage,and date/time
import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle
from datetime import datetime
from enum import Enum
# ------------------- ENUMS -------------------
#Defining each Enum class
class OrderStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

class PaymentStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    REFUNDED = "Refunded"
    FAILED = "Failed"

class TicketType(Enum):
    SINGLE_RACE = "Single Race"
    WEEKEND_PACKAGE = "Weekend Package"
    SEASON_MEMBERSHIP = "Season Membership"
    GROUP_DISCOUNT = "Group Discount"

class ReservationStatus(Enum):
    CONFIRMED = "Confirmed"
    PENDING = "Pending"
    CANCELLED = "Cancelled"

class RaceEventStatus(Enum):
    SCHEDULED = "Scheduled"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

# ------------------- File Storage -------------------
#These are the file paths that are used to store the data using the pickle
ACCOUNT_FILE = 'accounts.pkl'
TICKET_FILE = 'tickets.pkl'
ORDER_FILE = 'orders.pkl'
DISCOUNT_FILE = 'discounts.pkl'
EVENT_FILE = 'events.pkl'
RESERVATION_FILE = 'reservations.pkl'

# ------------------- Classes -------------------
#These classes are used to define the different attributes
class FanAccount:
    def __init__(self, name, email, phone, password):
        self.email = email
        self.name = name
        self.phone = phone
        self.password = password


    def update_details(self, name=None, phone=None, password=None):
        if name: self.name = name
        if phone: self.phone = phone
        if password: self.password = password

class AdminAccount:
    def __init__(self):
        self.username = 'admin'
        self.password = 'admin123'
        self.discount = 0.0

    def set_discount(self, value):
        self.discount = value

class RaceTicket:
    def __init__(self, ticket_type: TicketType, price, validity, features):
        self.ticket_type = ticket_type
        self.price = price
        self.validity = validity
        self.features = features

class TicketOrder:
    def __init__(self, fan_email, ticket_type: TicketType, quantity, price, payment_method):
        self.date = datetime.now()
        self.ticket_type = ticket_type
        self.quantity = quantity
        self.total = quantity * price
        self.fan_email = fan_email
        self.status = OrderStatus.CONFIRMED
        self.payment_status = PaymentStatus.COMPLETED
        self.payment_method = payment_method

class RaceEvent:
    def __init__(self, event_id, name, date, location, status=RaceEventStatus.SCHEDULED):
        self.event_id = event_id
        self.name = name
        self.date = date
        self.location = location
        self.status = status

class Reservation:
    def __init__(self, reservation_id, fan_email, event_id, seats, status=ReservationStatus.PENDING):
        self.reservation_id = reservation_id
        self.fan_email = fan_email
        self.event_id = event_id
        self.seats = seats
        self.status = status


# ------------------- File Helpers -------------------
#As we can see from the load_data function, we are basically loading the pickle files
def load_data(file):
    try:
        with open(file, 'rb') as f:
            return pickle.load(f)
    except:
        return {}
#Here we are saving the data to a pickle file
def save_data(file, data):
    with open(file, 'wb') as f:
        pickle.dump(data, f)

#Here we load all of the data
accounts = load_data(ACCOUNT_FILE)
tickets = load_data(TICKET_FILE)
orders = load_data(ORDER_FILE)
discounts = load_data(DISCOUNT_FILE)
admin_account = AdminAccount()
events = load_data(EVENT_FILE)
reservations = load_data(RESERVATION_FILE)

# ------------------- GUI App -------------------
#Here we have the main GUI class that will display the data and the classes we made
class TicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrated Ticketing System")
        self.user = None
        self.main_menu()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

#This shows the home main menu
    def main_menu(self):
        self.clear()
        tk.Label(self.root, text="Race Ticketing System", font=('Arial', 16)).pack(pady=10)
        tk.Button(self.root, text="Login", command=self.login_screen, width=25).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register_screen, width=25).pack(pady=5)
        tk.Button(self.root, text="Admin Login", command=self.admin_login_screen, width=25).pack(pady=5)

#This shows the regestration screen where new users can register
    def register_screen(self):
        self.clear()
        entries = {}
        tk.Label(self.root, text="Register", font=('Arial', 14)).pack(pady=10)
        for label in ["Name", "Email", "Phone", "Password"]:
            tk.Label(self.root, text=label).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[label] = entry

        def submit():
            name = entries["Name"].get()
            email = entries["Email"].get()
            phone = entries["Phone"].get()
            password = entries["Password"].get()
            if email in accounts:
                messagebox.showerror("Error", "Email already registered")
                return
            accounts[email] = FanAccount(name, email, phone, password)
            save_data(ACCOUNT_FILE, accounts)
            messagebox.showinfo("Success", "Account created")
            self.main_menu()

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

#This shows the login screen for the existing users where they can directly login
    def login_screen(self):
        self.clear()
        tk.Label(self.root, text="User Login", font=('Arial', 14)).pack(pady=10)
        email_entry = tk.Entry(self.root)
        pass_entry = tk.Entry(self.root, show='*')
        tk.Label(self.root, text="Email").pack()
        email_entry.pack()
        tk.Label(self.root, text="Password").pack()
        pass_entry.pack()

        def login():
            email = email_entry.get()
            password = pass_entry.get()
            user = accounts.get(email)
            if user and user.password == password:
                self.user = user
                self.user_dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(self.root, text="Login", command=login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

#This shows the dashboard for the user where they cna view events, buy tickets, or view existing reservations
    def user_dashboard(self):
        self.clear()
        tk.Label(self.root, text=f"Welcome {self.user.name}", font=('Arial', 14)).pack(pady=10)
        tk.Button(self.root, text="Buy Ticket", command=self.view_tickets).pack(pady=5)
        tk.Button(self.root, text="My Orders", command=self.view_orders).pack(pady=5)
        tk.Button(self.root, text="Edit Profile", command=self.edit_profile).pack(pady=5)
        tk.Button(self.root, text="My Reservations", command=self.view_reservations).pack(pady=5)
        tk.Button(self.root, text="Upcoming Events", command=self.view_events).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.main_menu).pack(pady=20)

#This helps the user in editing their profile if any changes are needed such as their phone number, email, name, and password
    def edit_profile(self):
        self.clear()
        tk.Label(self.root, text="Edit Profile", font=('Arial', 14)).pack(pady=10)
        name = tk.Entry(self.root)
        name.insert(0, self.user.name)
        phone = tk.Entry(self.root)
        phone.insert(0, self.user.phone)
        password = tk.Entry(self.root, show='*')
        password.insert(0, self.user.password)
        for label, entry in zip(["Name", "Phone", "Password"], [name, phone, password]):
            tk.Label(self.root, text=label).pack()
            entry.pack()
        #This updates the user's profile
        def save():
            self.user.update_details(name.get(), phone.get(), password.get())
            save_data(ACCOUNT_FILE, accounts)
            messagebox.showinfo("Updated", "Profile updated.")
            self.user_dashboard()

        tk.Button(self.root, text="Save", command=save).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.user_dashboard).pack()

#Shows the tickets the user have purchased
    def view_tickets(self):
        self.clear()
        tk.Label(self.root, text="Tickets", font=('Arial', 14)).pack(pady=10)
        for ticket_id, t in tickets.items():
            label = f"{t.ticket_type} - ${t.price} ({t.validity})"
            tk.Button(self.root, text=label, command=lambda t=t: self.buy_ticket(t)).pack(pady=2)
        tk.Button(self.root, text="Back", command=self.user_dashboard).pack(pady=10)

#Helps the user in purchasing the desired ticket
    def buy_ticket(self, ticket):
        qty = simpledialog.askinteger("Quantity", "Enter number of tickets:", minvalue=1, maxvalue=10)
        if qty:
            payment_method = simpledialog.askstring("Payment", "Enter payment method (e.g., credit/debit):")
            if not payment_method:
                messagebox.showwarning("Missing Info", "Payment method is required.")
                return
            order = TicketOrder(self.user.email, ticket.ticket_type, qty, ticket.price, payment_method)
            if self.user.email not in orders:
                orders[self.user.email] = []
            orders[self.user.email].append(order)
            save_data(ORDER_FILE, orders)
            save_data(ACCOUNT_FILE, accounts)
            messagebox.showinfo("Success", f"Order placed: ${order.total:.2f}")
            self.user_dashboard()

#This helps the user in viewing their orders
    def view_orders(self):
        self.clear()
        tk.Label(self.root, text="Your Orders", font=('Arial', 14)).pack(pady=10)

        user_orders = orders.get(self.user.email, [])
        for i, o in enumerate(user_orders):
            tk.Label(self.root, text=f"[{i + 1}] {o.ticket_type} x{o.quantity} = ${o.total:.2f}").pack()
#Here the user can delete existing orders
        def delete_order():
            idx = simpledialog.askinteger("Delete Order", "Enter order number to delete")
            if idx and 0 < idx <= len(user_orders):
                user_orders.pop(idx - 1)
                orders[self.user.email] = user_orders
                save_data(ORDER_FILE, orders)
                messagebox.showinfo("Deleted", "Order removed.")
                self.view_orders()


        tk.Button(self.root, text="Delete Order", command=delete_order).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.user_dashboard).pack(pady=10)

#This is the admin's login
    def admin_login_screen(self):
        self.clear()
        tk.Label(self.root, text="Admin Login", font=('Arial', 14)).pack(pady=10)
        u = tk.Entry(self.root)
        p = tk.Entry(self.root, show='*')
        tk.Label(self.root, text="Username").pack()
        u.pack()
        tk.Label(self.root, text="Password").pack()
        p.pack()
        def login():
            if u.get() == admin_account.username and p.get() == admin_account.password:
                self.admin_dashboard()
            else:
                messagebox.showerror("Error", "Incorrect admin credentials")
        tk.Button(self.root, text="Login", command=login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

#This is the admins dashboard where they can add the features that are required such as adding tickets, setting discounts, and viewing saled, and adding events.
    def admin_dashboard(self):
        self.clear()
        tk.Label(self.root, text="Admin Dashboard", font=('Arial', 14)).pack(pady=10)
        tk.Button(self.root, text="Add Ticket", command=self.add_ticket).pack(pady=5)
        tk.Button(self.root, text="Set Discount", command=self.set_discount).pack(pady=5)
        tk.Button(self.root, text="View Sales", command=self.view_sales).pack(pady=5)
        tk.Button(self.root, text="Add Event", command=self.add_event).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

#Here the admin can add the different types of tickets and their features.
    def add_ticket(self):
        self.clear()
        tk.Label(self.root, text="New Ticket Type", font=('Arial', 14)).pack(pady=10)
        type_var = tk.StringVar()
        tk.OptionMenu(self.root, type_var, *[t.value for t in TicketType]).pack()
        price = tk.Entry(self.root)
        validity = tk.Entry(self.root)
        features = tk.Entry(self.root)
        for lbl, entry in zip(["Price", "Validity", "Features"], [price, validity, features]):
            tk.Label(self.root, text=lbl).pack()
            entry.pack()
        def submit():
            try:
                enum_type = TicketType([t for t in TicketType if t.value == type_var.get()][0])
                t = RaceTicket(enum_type, float(price.get()), validity.get(), features.get())
                tickets[enum_type.name] = t
                save_data(TICKET_FILE, tickets)
                messagebox.showinfo("Added", "Ticket added successfully")
                self.admin_dashboard()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(self.root, text="Add Ticket", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack()

#Here the admin can set the discount between 0-1 where it converts it to percentage
    def set_discount(self):
        value = simpledialog.askfloat("Set Discount", "Enter discount percentage (0 to 1):")
        if value is not None:
            admin_account.set_discount(value)
            discounts['current'] = value
            save_data(DISCOUNT_FILE, discounts)
            messagebox.showinfo("Updated", f"Discount set to {value*100:.0f}%")

#Here the admin can view the purchased tickets by the users
    def view_sales(self):
        self.clear()
        tk.Label(self.root, text="Sales Report", font=('Arial', 14)).pack(pady=10)
        daily = {}
        for user_orders in orders.values():
            for o in user_orders:
                d = o.date.date()
                daily[d] = daily.get(d, 0) + o.quantity
        for d, qty in daily.items():
            tk.Label(self.root, text=f"{d}: {qty} tickets sold").pack()
        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack()

#Here the admin can create the events and add them on display to users dashboard
    def add_event(self):
        self.clear()
        tk.Label(self.root, text="Add Race Event", font=('Arial', 14)).pack(pady=10)

        entries = {}
        for label in ["Event ID", "Event Name", "Date (YYYY-MM-DD)", "Location"]:
            tk.Label(self.root, text=label).pack()
            e = tk.Entry(self.root)
            e.pack()
            entries[label] = e

        def submit():
            event_id = entries["Event ID"].get()
            name = entries["Event Name"].get()
            date = entries["Date (YYYY-MM-DD)"].get()
            location = entries["Location"].get()

            if event_id in events:
                messagebox.showerror("Error", "Event ID already exists")
                return

            event = RaceEvent(event_id, name, date, location)
            events[event_id] = event
            save_data(EVENT_FILE, events)
            messagebox.showinfo("Success", "Event added successfully")
            self.admin_dashboard()

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.admin_dashboard).pack(pady=5)

#Here the user can view the different events that are upcoming that has been displayed by the admin
    def view_events(self):
        self.clear()
        tk.Label(self.root, text="Upcoming Events", font=('Arial', 14)).pack(pady=10)
        if not events:
            tk.Label(self.root, text="No events available.").pack()
        for event in events.values():
            info = f"{event.name} | {event.date} @ {event.location} [{event.status.value}]"
            tk.Button(self.root, text=info, command=lambda e=event: self.reserve_event(e)).pack(pady=2)
        tk.Button(self.root, text="Back", command=self.user_dashboard).pack(pady=10)

#The user can reserve the event and select the number of seats ad desired.
    def reserve_event(self, event):
        seats = simpledialog.askinteger("Reserve Seats", "Number of seats:", minvalue=1, maxvalue=10)
        if not seats:
            return
        res_id = f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}"
        res = Reservation(res_id, self.user.email, event.event_id, seats)
        if self.user.email not in reservations:
            reservations[self.user.email] = []
        reservations[self.user.email].append(res)
        save_data(RESERVATION_FILE, reservations)
        messagebox.showinfo("Reserved", f"Reservation confirmed for {event.name}.")
        self.user_dashboard()

#The users can view the reservations they have made
    def view_reservations(self):
        self.clear()
        tk.Label(self.root, text="My Reservations", font=('Arial', 14)).pack(pady=10)
        res_list = reservations.get(self.user.email, [])
        if not res_list:
            tk.Label(self.root, text="No reservations found.").pack()
        for r in res_list:
            event = events.get(r.event_id)
            event_name = event.name if event else "Unknown Event"
            tk.Label(self.root, text=f"{event_name} | {r.seats} seats | Status: {r.status.value}").pack()
        tk.Button(self.root, text="Back", command=self.user_dashboard).pack(pady=10)

# ------------------- Run App -------------------
#This runs the GUI and displays it
if __name__ == '__main__':
    root = tk.Tk()
    app = TicketApp(root)
    root.mainloop()





