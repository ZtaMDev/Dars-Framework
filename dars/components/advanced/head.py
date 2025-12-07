# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev

from typing import List, Dict, Optional
from dars.core.component import Component


class Head(Component):
    """
    Define SEO metadata for a page. This component does not render visible content.
    
    The Head component allows you to customize HTML <head> metadata on a per-page basis,
    which is essential for SEO, social sharing, and proper page indexing.
    
    Features:
    - Basic SEO (title, description, keywords, author)
    - Open Graph tags for social sharing (Facebook, LinkedIn)
    - Twitter Card tags
    - Canonical URLs
    - Robots directives
    - Custom meta and link tags
    - JSON-LD structured data
    - Per-page favicon override
    
    Example:
        ```python
        from dars.all import *
        
        @route("/blog/post", route_type=RouteType.SSR)
        def blog_post():
            return Page(
                Head(
                    title="My Blog Post - My Site",
                    description="An amazing blog post about Python",
                    keywords=["python", "web", "framework"],
                    og_image="https://example.com/image.jpg",
                    og_type="article"
                ),
                Heading("My Blog Post", level=1),
                Text("Content here...")
            )
        ```
    
    Note:
        - This component does NOT handle CSS or JavaScript (handled by exporter)
        - It only manages metadata in the HTML <head> section
        - Multiple Head components: last one wins (or merge strategy)
    """
    
    def __init__(
        self,
        # Basic SEO
        title: str = None,
        description: str = None,
        keywords: List[str] = None,
        author: str = None,
        robots: str = None,  # "index, follow", "noindex, nofollow", etc.
        canonical: str = None,
        
        # Favicon (per-page override)
        favicon: str = None,
        
        # Open Graph (Facebook, LinkedIn, etc.)
        og_title: str = None,
        og_description: str = None,
        og_image: str = None,
        og_image_width: int = None,
        og_image_height: int = None,
        og_type: str = "website",  # article, product, etc.
        og_url: str = None,
        og_site_name: str = None,
        og_locale: str = None,
        
        # Twitter Card
        twitter_card: str = "summary",  # summary, summary_large_image, app, player
        twitter_site: str = None,  # @username
        twitter_creator: str = None,  # @username
        twitter_title: str = None,
        twitter_description: str = None,
        twitter_image: str = None,
        
        # Custom meta tags
        meta: List[Dict[str, str]] = None,
        
        # Link tags (alternate languages, etc.)
        links: List[Dict[str, str]] = None,
        
        # JSON-LD structured data
        structured_data: Dict = None,
        
        **kwargs
    ):
        """
        Initialize Head component with SEO metadata.
        
        Args:
            title: Page title (overrides app.title)
            description: Meta description for SEO
            keywords: List of keywords or comma-separated string
            author: Page author
            robots: Robots directive (e.g., "index, follow")
            canonical: Canonical URL for this page
            favicon: Favicon URL (overrides app.favicon)
            
            og_title: Open Graph title (defaults to title)
            og_description: Open Graph description (defaults to description)
            og_image: Open Graph image URL
            og_image_width: OG image width in pixels
            og_image_height: OG image height in pixels
            og_type: OG type (website, article, product, etc.)
            og_url: Canonical URL for OG
            og_site_name: Site name for OG
            og_locale: Locale for OG (e.g., "en_US")
            
            twitter_card: Twitter card type
            twitter_site: Twitter site handle (@username)
            twitter_creator: Twitter creator handle (@username)
            twitter_title: Twitter card title (defaults to og_title or title)
            twitter_description: Twitter card description
            twitter_image: Twitter card image URL
            
            meta: List of custom meta tags as dicts
            links: List of custom link tags as dicts
            structured_data: JSON-LD structured data as dict
        """
        super().__init__(**kwargs)
        
        # Basic SEO
        self.title = title
        self.description = description
        self.keywords = keywords
        self.author = author
        self.robots = robots
        self.canonical = canonical
        
        # Favicon
        self.favicon = favicon
        
        # Open Graph (smart defaults)
        self.og_title = og_title or title
        self.og_description = og_description or description
        self.og_image = og_image
        self.og_image_width = og_image_width
        self.og_image_height = og_image_height
        self.og_type = og_type
        self.og_url = og_url
        self.og_site_name = og_site_name
        self.og_locale = og_locale
        
        # Twitter (smart defaults)
        self.twitter_card = twitter_card
        self.twitter_site = twitter_site
        self.twitter_creator = twitter_creator
        self.twitter_title = twitter_title or og_title or title
        self.twitter_description = twitter_description or og_description or description
        self.twitter_image = twitter_image or og_image
        
        # Custom
        self.meta = meta or []
        self.links = links or []
        self.structured_data = structured_data
    
    def __repr__(self):
        """String representation for debugging"""
        title_str = f"title='{self.title}'" if self.title else "no title"
        return f"Head({title_str})"
