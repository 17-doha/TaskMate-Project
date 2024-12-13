# TaskMate

## Table of Contents
- [Project Overview](#Project-overview)
- [Installation](#Installation)
- [Features](#Features)
- [Contributing](#contributing)

## Project Overview
TaskMate is a task management and collaboration tool designed to help teams and individuals stay organized and productive. It allows users to create environments, manage tasks, and collaborate in a simple, visually engaging way. With features such as user registration, theme management, task creation, and real-time notifications, TaskMate provides a streamlined way to manage personal and team tasks.

## phase 3 vid
[From here](https://drive.google.com/file/d/1TZ9GOQ9J_V8hCet78d7xoy2-B11FA5j0/view?usp=sharing)

## Installation

### Prerequisites
- Python 3.x
- Django

### Steps to Set Up Locally

1. Clone the repository:
```bash
   git clone https://github.com/your-username/taskmate.git
```

2. Create a Virtual Environment (Recommended): It's a good practice to use a virtual environment to manage project dependencies:
```bash
python -m venv venv
```

- On Mac/Linux:
```bash
source venv/bin/activate
```

3. exit the venv
```bash
cd..
```

4. Navigate to the project directory:
```bash
cd taskmate
```

5. Setup the database
```bash
py manage.py makemigrations
```

6. Migrate
```bash
py manage.py migrate
```

7. Install dependencies
```bash
pip install -r requirements.txt
```

8. Run the development server: Start the Django development server:
```bash
python manage.py runserver
```

9. Access TaskMate in the browser: Open your browser and navigate to `http://127.0.0.1:8000/` to view TaskMate locally.


## Features

### User Registration/Login
- Register or login using Google or email.
- Email verification is sent upon registration for verification.

### Password Recovery
- Users can reset their password by receiving a password recovery link via email.

### Theme Management
- Toggle between dark and light themes via the navigation bar for personalized display preferences.

### User Profile Management
- View, edit, and delete profile information.
- View badges earned based on completed tasks.

### Environment Creation
- Create new task environments with default tables (To-Do, In Progress, Completed).

### Environment Sharing and Access Control
- Share environments by inviting others to collaborate.
- Set access permissions for shared environments, including view-only access.

### Environment Search
- Search for environments by name or keyword.
- Open the selected environment for task management.

### Environment Invitation
- Invite others to join an environment by sending them a link for view-only access.

### Participant Management
- View a list of all participants within an environment.

### Dashboard Display
- The dashboard shows the number of upcoming deadlines, in-progress tasks, overdue tasks, and the progress of the top environments.

### Task Creation
- Create tasks within an environment, specifying task labels, priority, and deadline dates.

### Task Assignment
- In shared environments, admins can assign tasks to specific participants.

### Participants Accessibility
- For shared environments, participants can view tasks and mark tasks as completed.

### Task Search
- Search tasks by title or keyword to view specific task details.

### Task Sorting by Priority
- Sort tasks within each table by priority for efficient management.

### Task Drag-and-Drop
- Drag and drop tasks between tables (To-Do, In Progress, Completed) to update task status.

### Task Manipulation
- Edit task details such as label, priority, assignments, and delete tasks from any table.

### Real-Time Notifications
- Receive notifications for task invitations, assignments, approaching deadlines, and task completions.

### Notification History
- Maintain a log of past notifications that users can access.

### Badges
- Earn badges based on the number of completed tasks.


## Contributing

We are grateful to the following contributors who have created this project:

- **Doha Hemdan**  
  [LinkedIn](https://www.linkedin.com/in/dohahemdan9838751b3/) | [GitHub](https://github.com/17-doha)
  
- **Haneen Alaa**  
  [LinkedIn](https://www.linkedin.com/in/haneen-alaa-44342b264/) | [GitHub](https://github.com/haneenalaa465)
  
- **Sara Elsayed**  
  [LinkedIn](https://www.linkedin.com/in/sarah-elsayed-20aab5284/) | [GitHub](https://github.com/selsayed2003)
  
- **Mariam Elghandour**  
  [LinkedIn](https://www.linkedin.com/in/mariam-elghandoor-271489255/) | [GitHub](https://github.com/mariamelghandoor)
  
- **Salma Sherif**  
  [LinkedIn](https://www.linkedin.com/in/salma-sherif-9b428a246/) | [GitHub](https://github.com/SalmaSherif7070)

Feel free to reach out to any of us for contributions or discussions on the project!
