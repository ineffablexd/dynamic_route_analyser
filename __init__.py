
def classFactory(iface):
    from .route_checker import dynamicRouteChecker
    return dynamicRouteChecker(iface)
