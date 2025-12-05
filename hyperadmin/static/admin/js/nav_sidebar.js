'use strict';
/** Everything is the same the original version apart from the initSidebarQuickFilter function. */
{
        /** This method hides sidebar items and item groups. */
        function initSidebarQuickFilter() {
            const options = [];
            const navSidebar = document.getElementById('mrl-nav-sidebar-content');
            if (!navSidebar) {
                return;
            }
            navSidebar.querySelectorAll('th[scope=row] a').forEach((container) => {
                options.push({title: container.innerHTML, node: container});
            });

            function checkValue(event) {
                let filterValue = event.target.value;
                if (filterValue) {
                    filterValue = filterValue.toLowerCase();
                }
                if (event.key === 'Escape') {
                    filterValue = '';
                    event.target.value = ''; // clear input
                }
                let isMatched = false;
                let matches = [];
                for (const o of options) {
                    let displayValue = '';
                    if (filterValue) {
                        if (o.title.toLowerCase().indexOf(filterValue) === -1) {
                            displayValue = 'none';
                        } else {
                            isMatched = true;
                            matches.push(o);
                        }
                    }
                    // show/hide parent <TR>
                    o.node.parentNode.parentNode.style.display = displayValue;
                    o.node.parentNode.parentNode.parentNode.parentNode.parentNode.style.display = displayValue;
                }
                // IT is ugly it should hide the right things at the first time now it hides to greedly and unhides everything
                for (const match of matches) {
                    match.node.parentNode.parentNode.style.display = '';
                    match.node.parentNode.parentNode.parentNode.parentNode.parentNode.style.display = '';
                }
                if (!filterValue || isMatched) {
                    event.target.classList.remove('no-results');
                } else {
                    event.target.classList.add('no-results');
                }
                sessionStorage.setItem('django.admin.navSidebarFilterValue', filterValue);
            }

            const nav = document.getElementById('nav-filter');
            nav.addEventListener('change', checkValue, false);
            nav.addEventListener('input', checkValue, false);
            nav.addEventListener('keyup', checkValue, false);

            const storedValue = sessionStorage.getItem('django.admin.navSidebarFilterValue');
            if (storedValue) {
                nav.value = storedValue;
                checkValue({target: nav, key: ''});
            }
        }
        window.initSidebarQuickFilter = initSidebarQuickFilter;
        initSidebarQuickFilter();
}
