
def classFactory(iface):
    from .route_checker import SmartRouteChecker
    return SmartRouteChecker(iface)
