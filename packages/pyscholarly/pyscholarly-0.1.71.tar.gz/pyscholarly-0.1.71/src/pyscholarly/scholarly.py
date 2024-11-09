from playwright.async_api import async_playwright
from datetime import datetime
import re
import asyncio
from typing import Dict, List, Optional, Union, Any
from kew import TaskQueueManager, QueueConfig, QueuePriority, TaskStatus
import logging
from logging import Logger
import random
from pathlib import Path

class ProxyRotator:
    def __init__(self, proxies: Optional[Union[str, List[str]]] = None):
        if isinstance(proxies, str):
            proxies = [proxies]
        
        self.proxies = []
        if proxies:
            for proxy in proxies:
                # Keep the original format, don't modify it
                self.proxies.append(proxy)
        
        self._current_index = 0

    def get_next(self) -> Optional[str]:
        if not self.proxies:
            return None
        proxy = self.proxies[self._current_index]
        self._current_index = (self._current_index + 1) % len(self.proxies)
        return proxy

    def get_random(self) -> Optional[str]:
        return random.choice(self.proxies) if self.proxies else None

class Scholar:
    def __init__(
        self, 
        logger: Optional[Logger] = None, 
        proxies: Optional[Union[str, List[str]]] = None,
        headless: bool = False,
        proxy_rotation: str = 'sequential'
    ):
        self._playwright = None
        self._browser = None
        self.logger = logger or logging.getLogger(__name__)
        self.proxy_rotator = ProxyRotator(proxies)
        self.headless = headless
        self.proxy_rotation = proxy_rotation

    async def _create_browser_context(self, proxy: Optional[str] = None):
        browser_args = {
            "viewport": {"width": 1920, "height": 1080},
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "java_script_enabled": True,
        }
        
        if proxy:
            self.logger.debug(f"Using proxy: {proxy}")
            try:
                if '@' in proxy:
                    # Handle proxy with traditional username:password@host:port format
                    proxy_parts = proxy.split('@')
                    if len(proxy_parts) == 2:
                        auth_part = proxy_parts[0].replace('http://', '')
                        server_part = proxy_parts[1]
                        
                        if ':' in auth_part:
                            username, password = auth_part.split(':')
                            browser_args["proxy"] = {
                                "server": f"http://{server_part}",
                                "username": username,
                                "password": password
                            }
                else:
                    # Handle IP:PORT:USERNAME:PASSWORD format
                    parts = proxy.split(':')
                    if len(parts) == 4:
                        host = parts[0]
                        port = parts[1]
                        username = parts[2]
                        password = parts[3]
                        
                        browser_args["proxy"] = {
                            "server": f"http://{host}:{port}",
                            "username": username,
                            "password": password
                        }
                    else:
                        # Handle simple host:port format
                        proxy_server = proxy if proxy.startswith('http://') or proxy.startswith('https://') else f"http://{proxy}"
                        browser_args["proxy"] = {
                            "server": proxy_server
                        }
            except Exception as e:
                self.logger.error(f"Error parsing proxy configuration: {e}")
        
        try:
            return await self._browser.new_context(**browser_args)
        except Exception as e:
            self.logger.error(f"Error creating browser context with proxy: {e}")
            # Fallback to no proxy if there's an error
            self.logger.warning("Falling back to no proxy")
            return await self._browser.new_context(**{k:v for k,v in browser_args.items() if k != 'proxy'})
    async def __aenter__(self):
        self.logger.info("Initializing Scholar session")
        self._playwright = await async_playwright().start()
        
        # Add additional arguments for true headless mode
        browser_args = {
            "headless": self.headless,
        }
        if self.headless:
            browser_args.update({
                "args": [
                    '--disable-gpu',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-setuid-sandbox',
                    '--no-first-run',
                    '--no-zygote',
                    '--deterministic-fetch',
                    '--disable-features=IsolateOrigins',
                    '--disable-site-isolation-trials',
                ]
            })
        
        self._browser = await self._playwright.chromium.launch(**browser_args)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("Closing Scholar session")
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    def _get_proxy(self) -> Optional[str]:
        if self.proxy_rotation == 'random':
            return self.proxy_rotator.get_random()
        return self.proxy_rotator.get_next()

    async def _get_page_content(self, url: str, context) -> str:
        self.logger.debug(f"Fetching content from {url}")
        page = await context.new_page()
        
        try:
            await page.goto(url)
            await page.wait_for_selector("#gsc_rsb_cit")
            content = await page.content()
            return content
        except Exception as e:
            self.logger.error(f"Error fetching page content: {e}")
            raise
        finally:
            await page.close()

    async def _get_ytd_citations(self, citation_link: str, context) -> int:
        if not citation_link:
            return 0
            
        self.logger.debug(f"Getting YTD citations from link: {citation_link}")
        
        try:
            page = await context.new_page()
            base_url = "https://scholar.google.com"
            await page.goto(f"{base_url}{citation_link}")
            
            # Modified selector to be more specific and removed visibility check
            year_citation_selector = 'a.gsc_oci_g_a[href*="as_ylo=2024"][href*="as_yhi=2024"] span.gsc_oci_g_al'
            try:
                # Wait for element to be present in DOM, not necessarily visible
                await page.wait_for_selector(year_citation_selector, state='attached', timeout=5000)
                ytd_element = await page.query_selector(year_citation_selector)
                if ytd_element:
                    ytd_text = await ytd_element.text_content()
                    ytd_count = int(ytd_text)
                    self.logger.info(f"Found {ytd_count} citations for 2024")
                    return ytd_count
            except Exception as e:
                self.logger.warning(f"Could not find 2024 citation element: {e}")
                return 0
                
        finally:
            await page.close()
    async def get_author_data(self, scholar_id: str) -> Dict:
        self.logger.info(f"Fetching author data for scholar ID: {scholar_id}")
        url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en&pagesize=100&view_op=list_works"
        
        proxy = self._get_proxy()
        context = await self._create_browser_context(proxy)
        
        try:
            content = await self._get_page_content(url, context)
            page = await context.new_page()
            await page.set_content(content)

            author_info = await page.evaluate('''() => {
                const name = document.querySelector("#gsc_prf_in")?.innerText || "";
                
                const stats = {};
                const rows = document.querySelectorAll("#gsc_rsb_st tbody tr");
                rows.forEach(row => {
                    const label = row.querySelector(".gsc_rsb_sc1 .gsc_rsb_f")?.innerText;
                    const values = Array.from(row.querySelectorAll(".gsc_rsb_std"));
                    if (label && values.length >= 2) {
                        stats[label] = {
                            all: parseInt(values[0].innerText) || 0,
                            recent: parseInt(values[1].innerText) || 0
                        };
                    }
                });
                
                return { name, stats };
            }''')

            publications = []
            last_count = 0
            
            while True:
                pub_data = await page.evaluate('''() => {
                    const pubs = Array.from(document.querySelectorAll('#gsc_a_b .gsc_a_tr'));
                    return pubs.map(pub => ({
                        title: pub.querySelector('.gsc_a_at')?.innerText || '',
                        citations: pub.querySelector('.gsc_a_ac')?.innerText || '0',
                        citation_link: pub.querySelector('.gsc_a_at')?.getAttribute('href') || null,  // Changed to get href from title
                        year: pub.querySelector('.gsc_a_y .gsc_a_h')?.innerText || '',
                        authors: pub.querySelectorAll('.gs_gray')[0]?.innerText || '',
                        venue: pub.querySelectorAll('.gs_gray')[1]?.innerText || ''
                    }));
                }''')


                current_count = len(pub_data)
                if current_count == last_count:
                    break

                for pub in pub_data[last_count:]:
                    try:
                        citation_count = int(pub['citations']) if pub['citations'] and pub['citations'] != '' else 0
                    except ValueError:
                        citation_count = 0

                    # Changed from paper_link to citation_link to match the evaluation
                    ytd_citations = await self._get_ytd_citations(pub['citation_link'], context) if pub['citation_link'] else 0

                    publications.append({
                        'title': pub['title'],
                        'authors': pub['authors'],
                        'venue': pub['venue'],
                        'num_citations': citation_count,
                        'ytd_citations': ytd_citations,
                        'year': pub['year']
                    })

                last_count = current_count
                
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                try:
                    await page.wait_for_function(
                        'document.querySelectorAll("#gsc_a_b .gsc_a_tr").length > arguments[0]',
                        arg=current_count,
                        timeout=3000
                    )
                except:
                    break

            return {
                'name': author_info['name'],
                'citations': author_info['stats'].get('Citations', {'all': 0, 'recent': 0}),
                'h_index': author_info['stats'].get('h-index', {'all': 0, 'recent': 0}),
                'i10_index': author_info['stats'].get('i10-index', {'all': 0, 'recent': 0}),
                'publications': publications
            }

        finally:
            await page.close()
            await context.close()

    @staticmethod
    def format_response(author_data: Dict) -> Dict:
        publications = []
        for pub in author_data['publications']:
            publications.append({
                'bib': {
                    'title': pub['title'],
                    'authors': pub['authors'],
                    'venue': pub['venue']
                },
                'num_citations': pub['num_citations'],
                'ytd_citations': pub['ytd_citations'],
                'year': pub.get('year', '')
            })

        return {
            'name': author_data['name'],
            'citedby': author_data['citations']['all'],
            'citedby_recent': author_data['citations']['recent'],
            'hindex': author_data['h_index']['all'],
            'hindex_recent': author_data['h_index']['recent'],
            'i10index': author_data['i10_index']['all'],
            'i10index_recent': author_data['i10_index']['recent'],
            'publications': publications
        }

async def fetch_scholar_data(
    scholar_id: str, 
    logger: Optional[Logger] = None,
    proxies: Optional[Union[str, List[str]]] = None,
    headless: bool = False,
    proxy_rotation: str = 'sequential'
) -> Dict:
    async with Scholar(
        logger=logger, 
        proxies=proxies, 
        headless=headless,
        proxy_rotation=proxy_rotation
    ) as scraper:
        author_data = await scraper.get_author_data(scholar_id)
        return Scholar.format_response(author_data)

# New function to handle multiple scholars
async def fetch_multiple_scholars(
    scholar_ids: List[str],
    logger: Optional[Logger] = None,
    proxies: Optional[Union[str, List[str]]] = None,
    headless: bool = False,
    proxy_rotation: str = 'sequential',
    max_workers: int = 3,
    redis_url: str = "redis://localhost:6379"
) -> List[Dict]:
    """
    Fetch data for multiple scholars using a task queue for parallel processing
    """
    # Initialize task queue manager
    queue_manager = TaskQueueManager(redis_url=redis_url)
    await queue_manager.initialize()
    
    # Create queue configuration
    queue_config = QueueConfig(
        name="scholar_queue",
        max_workers=max_workers,
        max_size=1000,
        priority=QueuePriority.MEDIUM
    )
    await queue_manager.create_queue(queue_config)
    
    # Initialize Scholar instance to be shared across workers
    scholar = Scholar(
        logger=logger,
        proxies=proxies,
        headless=headless,
        proxy_rotation=proxy_rotation
    )
    
    async def process_scholar(scholar_id: str) -> Dict:
        """Worker function to process individual scholar"""
        try:
            async with scholar:
                author_data = await scholar.get_author_data(scholar_id)
                return Scholar.format_response(author_data)
        except Exception as e:
            logger.error(f"Error processing scholar {scholar_id}: {e}")
            return None

    try:
        # Submit tasks for each scholar
        tasks = []
        for scholar_id in scholar_ids:
            task_id = f"scholar_{scholar_id}"
            task_info = await queue_manager.submit_task(
                task_id=task_id,
                queue_name="scholar_queue",
                task_type="scholar_fetch",
                task_func=process_scholar,
                priority=QueuePriority.MEDIUM,
                scholar_id=scholar_id
            )
            tasks.append(task_info)

        # Wait for all tasks to complete
        results = []
        for task in tasks:
            while True:
                task_info = await queue_manager.get_task_status(task.task_id)
                if task_info.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                    results.append(task_info.result)
                    break
                await asyncio.sleep(0.1)

        return results

    finally:
        # Cleanup
        await queue_manager.shutdown()