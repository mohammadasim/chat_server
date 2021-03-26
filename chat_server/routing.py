from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing


"""
This routing configuration specifies that when a connection is made to the 
Channels development server, the ProtocolTypeRouter will first inspect the 
type of connection. If it is a Websocket connection (ws:// or wss://), the 
connection will be given to the AuthMiddlewareStack.
The AuthMiddlewareStack will populate the connection's scope with a reference
to the currently authenticated user, similar to how Django's AuthenticationMiddleware
populates the request object of a view function with the currently authenticated user.
Then the connection will be given to URLRouter.
The URLRouter will examine the HTTP path of the connection to route it to a particular
consumer, based on the provided url patterns.
"""
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
