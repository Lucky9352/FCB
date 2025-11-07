/**
 * TapNex Arena - Responsive Debug Helper
 * Development tool for testing responsive design
 * Remove or disable in production
 */

(function () {
    'use strict';

    // Only run in development (check for localhost or specific flag)
    const isDevelopment = window.location.hostname === 'localhost' ||
        window.location.hostname === '127.0.0.1' ||
        window.location.search.includes('debug=true');

    if (!isDevelopment) {
        console.log('Responsive debug tools disabled in production');
        return;
    }

    console.log('🔧 Responsive Debug Tools Loaded');

    // ============================================
    // VIEWPORT SIZE TRACKER
    // ============================================
    function updateViewportInfo() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        const orientation = width > height ? 'Landscape' : 'Portrait';

        let breakpoint = 'Unknown';
        if (width < 375) breakpoint = 'Small Mobile';
        else if (width < 640) breakpoint = 'Mobile';
        else if (width < 768) breakpoint = 'Tablet Small';
        else if (width < 1024) breakpoint = 'Tablet';
        else if (width < 1280) breakpoint = 'Desktop';
        else if (width < 1536) breakpoint = 'Desktop Large';
        else breakpoint = 'Desktop XL';

        console.log(`📐 Viewport: ${width}x${height} | ${breakpoint} | ${orientation}`);

        // Update body data attributes
        document.body.setAttribute('data-width', width);
        document.body.setAttribute('data-height', height);
        document.body.setAttribute('data-breakpoint', breakpoint);
        document.body.setAttribute('data-orientation', orientation);
    }

    updateViewportInfo();
    window.addEventListener('resize', updateViewportInfo);
    window.addEventListener('orientationchange', updateViewportInfo);

    // ============================================
    // TOUCH TARGET CHECKER
    // ============================================
    function checkTouchTargets() {
        const minSize = 44; // iOS recommended minimum
        const elements = document.querySelectorAll('a, button, input, select');
        const smallTargets = [];

        elements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.width < minSize || rect.height < minSize) {
                smallTargets.push({
                    element: el,
                    width: Math.round(rect.width),
                    height: Math.round(rect.height),
                    text: el.textContent?.trim().substring(0, 30) || el.tagName
                });
            }
        });

        if (smallTargets.length > 0) {
            console.warn(`⚠️ Found ${smallTargets.length} touch targets smaller than ${minSize}px:`);
            console.table(smallTargets.map(t => ({
                text: t.text,
                width: t.width,
                height: t.height,
                tag: t.element.tagName
            })));
        } else {
            console.log('✅ All touch targets meet minimum size requirements');
        }
    }

    // ============================================
    // RESPONSIVE IMAGE CHECKER
    // ============================================
    function checkResponsiveImages() {
        const images = document.querySelectorAll('img');
        const issues = [];

        images.forEach(img => {
            const hasMaxWidth = window.getComputedStyle(img).maxWidth === '100%';
            const hasHeight = img.style.height && img.style.height !== 'auto';

            if (!hasMaxWidth) {
                issues.push({
                    src: img.src.substring(img.src.lastIndexOf('/') + 1),
                    issue: 'Missing max-width: 100%'
                });
            }

            if (hasHeight) {
                issues.push({
                    src: img.src.substring(img.src.lastIndexOf('/') + 1),
                    issue: 'Has fixed height (should be auto)'
                });
            }
        });

        if (issues.length > 0) {
            console.warn(`⚠️ Found ${issues.length} image responsiveness issues:`);
            console.table(issues);
        } else {
            console.log('✅ All images are responsive');
        }
    }

    // ============================================
    // HORIZONTAL SCROLL CHECKER
    // ============================================
    function checkHorizontalScroll() {
        const bodyWidth = document.body.scrollWidth;
        const windowWidth = window.innerWidth;

        if (bodyWidth > windowWidth) {
            console.error(`❌ Horizontal scroll detected! Body width (${bodyWidth}px) > Window width (${windowWidth}px)`);

            // Find elements causing overflow
            const elements = document.querySelectorAll('*');
            const overflowing = [];

            elements.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.right > windowWidth) {
                    overflowing.push({
                        element: el.tagName,
                        class: el.className,
                        width: Math.round(rect.width),
                        right: Math.round(rect.right)
                    });
                }
            });

            if (overflowing.length > 0) {
                console.warn('Elements causing overflow:');
                console.table(overflowing.slice(0, 10)); // Show first 10
            }
        } else {
            console.log('✅ No horizontal scroll detected');
        }
    }

    // ============================================
    // FONT SIZE CHECKER
    // ============================================
    function checkFontSizes() {
        const minSize = 14; // Minimum readable size on mobile
        const elements = document.querySelectorAll('p, span, a, button, li, td, th');
        const tooSmall = [];

        elements.forEach(el => {
            const fontSize = parseFloat(window.getComputedStyle(el).fontSize);
            if (fontSize < minSize && el.textContent.trim()) {
                tooSmall.push({
                    text: el.textContent.trim().substring(0, 30),
                    fontSize: Math.round(fontSize),
                    tag: el.tagName
                });
            }
        });

        if (tooSmall.length > 0) {
            console.warn(`⚠️ Found ${tooSmall.length} elements with font size < ${minSize}px:`);
            console.table(tooSmall.slice(0, 10));
        } else {
            console.log('✅ All text meets minimum font size');
        }
    }

    // ============================================
    // PERFORMANCE CHECKER
    // ============================================
    function checkPerformance() {
        if ('performance' in window) {
            const perfData = window.performance.timing;
            const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
            const domReadyTime = perfData.domContentLoadedEventEnd - perfData.navigationStart;

            console.log('⚡ Performance Metrics:');
            console.log(`  Page Load Time: ${pageLoadTime}ms`);
            console.log(`  DOM Ready Time: ${domReadyTime}ms`);

            if (pageLoadTime > 3000) {
                console.warn('⚠️ Page load time is slow (> 3s)');
            } else {
                console.log('✅ Page load time is good');
            }
        }
    }

    // ============================================
    // KEYBOARD SHORTCUTS
    // ============================================
    document.addEventListener('keydown', function (e) {
        // Ctrl+Shift+D - Toggle debug mode
        if (e.ctrlKey && e.shiftKey && e.key === 'D') {
            e.preventDefault();
            document.body.classList.toggle('show-debug-grid');
            console.log('🔧 Debug grid toggled');
        }

        // Ctrl+Shift+V - Toggle viewport size
        if (e.ctrlKey && e.shiftKey && e.key === 'V') {
            e.preventDefault();
            document.body.classList.toggle('show-viewport-size');
            console.log('🔧 Viewport size display toggled');
        }

        // Ctrl+Shift+T - Check touch targets
        if (e.ctrlKey && e.shiftKey && e.key === 'T') {
            e.preventDefault();
            checkTouchTargets();
        }

        // Ctrl+Shift+I - Check images
        if (e.ctrlKey && e.shiftKey && e.key === 'I') {
            e.preventDefault();
            checkResponsiveImages();
        }

        // Ctrl+Shift+S - Check horizontal scroll
        if (e.ctrlKey && e.shiftKey && e.key === 'S') {
            e.preventDefault();
            checkHorizontalScroll();
        }

        // Ctrl+Shift+F - Check font sizes
        if (e.ctrlKey && e.shiftKey && e.key === 'F') {
            e.preventDefault();
            checkFontSizes();
        }

        // Ctrl+Shift+P - Check performance
        if (e.ctrlKey && e.shiftKey && e.key === 'P') {
            e.preventDefault();
            checkPerformance();
        }

        // Ctrl+Shift+A - Run all checks
        if (e.ctrlKey && e.shiftKey && e.key === 'A') {
            e.preventDefault();
            console.log('🔍 Running all responsive checks...');
            checkTouchTargets();
            checkResponsiveImages();
            checkHorizontalScroll();
            checkFontSizes();
            checkPerformance();
        }
    });

    // ============================================
    // AUTO-RUN CHECKS ON LOAD
    // ============================================
    window.addEventListener('load', function () {
        setTimeout(function () {
            console.log('🔍 Running automatic responsive checks...');
            checkHorizontalScroll();
            checkPerformance();

            console.log('\n📋 Keyboard Shortcuts:');
            console.log('  Ctrl+Shift+D - Toggle debug grid');
            console.log('  Ctrl+Shift+V - Toggle viewport size');
            console.log('  Ctrl+Shift+T - Check touch targets');
            console.log('  Ctrl+Shift+I - Check images');
            console.log('  Ctrl+Shift+S - Check horizontal scroll');
            console.log('  Ctrl+Shift+F - Check font sizes');
            console.log('  Ctrl+Shift+P - Check performance');
            console.log('  Ctrl+Shift+A - Run all checks');
        }, 1000);
    });

    // ============================================
    // BREAKPOINT CHANGE LOGGER
    // ============================================
    let lastBreakpoint = null;

    function logBreakpointChange() {
        const currentBreakpoint = document.body.getAttribute('data-breakpoint');
        if (currentBreakpoint !== lastBreakpoint) {
            console.log(`📱 Breakpoint changed: ${lastBreakpoint || 'Initial'} → ${currentBreakpoint}`);
            lastBreakpoint = currentBreakpoint;
        }
    }

    window.addEventListener('resize', logBreakpointChange);
    logBreakpointChange();

    // ============================================
    // EXPOSE DEBUG FUNCTIONS GLOBALLY
    // ============================================
    window.responsiveDebug = {
        checkTouchTargets,
        checkResponsiveImages,
        checkHorizontalScroll,
        checkFontSizes,
        checkPerformance,
        runAllChecks: function () {
            console.log('🔍 Running all responsive checks...');
            checkTouchTargets();
            checkResponsiveImages();
            checkHorizontalScroll();
            checkFontSizes();
            checkPerformance();
        }
    };

    console.log('💡 Use window.responsiveDebug to access debug functions');
    console.log('💡 Example: responsiveDebug.runAllChecks()');

})();
