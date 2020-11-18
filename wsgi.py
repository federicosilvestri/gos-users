"""
Go Out Safe
Web Server Gateway Interface

This file is the entry point for
gooutsafe-users-ms microservice.
"""
from gooutsafe import create_app

# application instance
app = create_app()

if __name__ == '__main__':
    app.run()
