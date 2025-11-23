"""
Unit tests for SPA Routing - Phase 1 (Foundation)

Tests the @route decorator, SPARoute class, RouteNode class, 
and App modifications for SPA routing support.
"""

import unittest
from dars.all import *


class TestRouteDecorator(unittest.TestCase):
    """Test @route decorator functionality"""
    
    def test_route_decorator_basic(self):
        """Test that @route decorator adds route metadata"""
        @route("/test")
        def test_page():
            return Page(Container(Text("Test")))
        
        self.assertTrue(hasattr(test_page, '__dars_route__'))
        self.assertEqual(test_page.__dars_route__, "/test")
    
    def test_route_with_parameters(self):
        """Test route decorator with parameters"""
        @route("/user/:id")
        def user_page():
            return Page(Container(Text("User")))
        
        self.assertEqual(user_page.__dars_route__, "/user/:id")
    
    def test_nested_route(self):
        """Test route decorator for nested routes"""
        @route("/docs/getting-started")
        def docs_start():
            return Page(Container(Text("Getting Started")))
        
        self.assertEqual(docs_start.__dars_route__, "/docs/getting-started")


class TestSPARoute(unittest.TestCase):
    """Test SPARoute class"""
    
    def test_spa_route_creation(self):
        """Test basic SPARoute creation"""
        page = Page(Container(Text("Home")))
        spa_route = SPARoute(
            name="home",
            root=page,
            route="/home",
            title="Home Page"
        )
        
        self.assertEqual(spa_route.name, "home")
        self.assertEqual(spa_route.route, "/home")
        self.assertEqual(spa_route.title, "Home Page")
        self.assertEqual(spa_route.params, [])
    
    def test_parameter_extraction(self):
        """Test route parameter extraction"""
        page = Page(Container(Text("User")))
        spa_route = SPARoute(
            name="user",
            root=page,
            route="/user/:id"
        )
        
        self.assertEqual(spa_route.params, ["id"])
    
    def test_multiple_parameters(self):
        """Test extraction of multiple parameters"""
        page = Page(Container(Text("Post")))
        spa_route = SPARoute(
            name="post_edit",
            root=page,
            route="/user/:userId/post/:postId/edit"
        )
        
        self.assertEqual(spa_route.params, ["userId", "postId"])
    
    def test_route_matching_exact(self):
        """Test exact route matching"""
        page = Page(Container(Text("About")))
        spa_route = SPARoute(
            name="about",
            root=page,
            route="/about"
        )
        
        result = spa_route.matches("/about")
        self.assertIsNotNone(result)
        self.assertEqual(result, {})
    
    def test_route_matching_with_param(self):
        """Test route matching with parameters"""
        page = Page(Container(Text("User")))
        spa_route = SPARoute(
            name="user",
            root=page,
            route="/user/:id"
        )
        
        result = spa_route.matches("/user/123")
        self.assertIsNotNone(result)
        self.assertEqual(result, {"id": "123"})
    
    def test_route_matching_multiple_params(self):
        """Test route matching with multiple parameters"""
        page = Page(Container(Text("Post")))
        spa_route = SPARoute(
            name="post",
            root=page,
            route="/user/:userId/post/:postId"
        )
        
        result = spa_route.matches("/user/42/post/99")
        self.assertIsNotNone(result)
        self.assertEqual(result, {"userId": "42", "postId": "99"})
    
    def test_route_not_matching(self):
        """Test that non-matching paths return None"""
        page = Page(Container(Text("Home")))
        spa_route = SPARoute(
            name="home",
            root=page,
            route="/home"
        )
        
        result = spa_route.matches("/about")
        self.assertIsNone(result)


class TestAppSPARouting(unittest.TestCase):
    """Test App class SPA routing integration"""
    
    def test_add_page_with_route_parameter(self):
        """Test adding page with route parameter"""
        app = App(title="Test App")
        page = Page(Container(Text("Home")))
        
        app.add_page("home", page, route="/")
        
        self.assertTrue(app.has_spa_routes())
        self.assertIn("home", app._spa_routes)
        self.assertEqual(app._spa_routes["home"].route, "/")
    
    def test_add_page_with_route_decorator(self):
        """Test adding page with @route decorator"""
        app = App(title="Test App")
        
        @route("/about")
        def about():
            return Page(Container(Text("About")))
        
        app.add_page("about", about())
        
        self.assertTrue(app.has_spa_routes())
        self.assertIn("about", app._spa_routes)
    
    def test_route_conflict_detection(self):
        """Test that defining route in both places raises error"""
        app = App(title="Test App")
        
        @route("/conflict")
        def conflict_page():
            return Page(Container(Text("Conflict")))
        
        with self.assertRaises(ValueError) as context:
            app.add_page("conflict", conflict_page(), route="/different")
        
        self.assertIn("defined in both", str(context.exception))
    
    def test_preload_without_route_error(self):
        """Test that preload without route raises error"""
        app = App(title="Test App")
        page = Page(Container(Text("Test")))
        
        with self.assertRaises(ValueError) as context:
            app.add_page("test", page, preload=["/other"])
        
        self.assertIn("preload parameter cannot be used without route", str(context.exception))
    
    def test_parent_without_route_error(self):
        """Test that parent without route raises error"""
        app = App(title="Test App")
        page = Page(Container(Text("Test")))
        
        with self.assertRaises(ValueError) as context:
            app.add_page("test", page, parent="docs")
        
        self.assertIn("parent parameter cannot be used without route", str(context.exception))
    
    def test_nested_routes(self):
        """Test nested route creation"""
        app = App(title="Test App")
        
        docs_page = Page(Container(Text("Docs")))
        start_page = Page(Container(Text("Getting Started")))
        
        app.add_page("docs", docs_page, route="/docs")
        app.add_page("docs_start", start_page, route="/docs/getting-started", parent="docs")
        
        self.assertEqual(len(app._spa_routes), 2)
        self.assertEqual(app._spa_routes["docs_start"].parent, "docs")
    
    def test_parent_must_exist(self):
        """Test that parent route must exist before child"""
        app = App(title="Test App")
        page = Page(Container(Text("Child")))
        
        with self.assertRaises(ValueError) as context:
            app.add_page("child", page, route="/docs/child", parent="docs")
        
        self.assertIn("Parent route", str(context.exception))
    
    def test_set_404_page(self):
        """Test setting custom 404 page"""
        app = App(title="Test App")
        not_found = Page(Container(Text("404 Not Found")))
        
        app.set_404_page(not_found)
        
        self.assertIsNotNone(app._spa_404_page)
        self.assertEqual(app._spa_404_page, not_found)
    
    def test_traditional_multipage_still_works(self):
        """Test that traditional multipage mode still works"""
        app = App(title="Test App")
        page1 = Page(Container(Text("Page 1")))
        page2 = Page(Container(Text("Page 2")))
        
        app.add_page("page1", page1, index=True)
        app.add_page("page2", page2)
        
        self.assertTrue(app.is_multipage())
        self.assertFalse(app.has_spa_routes())
        self.assertEqual(len(app.pages), 2)
    
    def test_hybrid_mode(self):
        """Test hybrid mode (traditional + SPA)"""
        app = App(title="Test App")
        
        # Traditional page
        trad_page = Page(Container(Text("Traditional")))
        app.add_page("traditional", trad_page)
        
        # SPA route
        spa_page = Page(Container(Text("SPA")))
        app.add_page("spa", spa_page, route="/spa")
        
        self.assertTrue(app.is_multipage())
        self.assertTrue(app.has_spa_routes())
        self.assertEqual(len(app.pages), 1)
        self.assertEqual(len(app._spa_routes), 1)


class TestRouteNode(unittest.TestCase):
    """Test RouteNode class for nested routes"""
    
    def test_route_node_creation(self):
        """Test RouteNode creation"""
        page = Page(Container(Text("Home")))
        spa_route = SPARoute(name="home", root=page, route="/")
        node = RouteNode(spa_route)
        
        self.assertEqual(node.route, spa_route)
        self.assertEqual(len(node.children), 0)
    
    def test_add_child(self):
        """Test adding child node"""
        parent_page = Page(Container(Text("Docs")))
        parent_route = SPARoute(name="docs", root=parent_page, route="/docs")
        parent_node = RouteNode(parent_route)
        
        child_page = Page(Container(Text("Start")))
        child_route = SPARoute(name="start", root=child_page, route="/docs/start")
        child_node = RouteNode(child_route)
        
        parent_node.add_child(child_node)
        
        self.assertEqual(len(parent_node.children), 1)
        self.assertEqual(parent_node.children[0], child_node)
    
    def test_find_route(self):
        """Test finding route in tree"""
        # Create tree structure
        root = RouteNode()
        
        home_page = Page(Container(Text("Home")))
        home_route = SPARoute(name="home", root=home_page, route="/")
        home_node = RouteNode(home_route)
        root.add_child(home_node)
        
        docs_page = Page(Container(Text("Docs")))
        docs_route = SPARoute(name="docs", root=docs_page, route="/docs")
        docs_node = RouteNode(docs_route)
        root.add_child(docs_node)
        
        # Find route
        result = root.find_route("/docs")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], docs_route)
        self.assertEqual(result[1], {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
