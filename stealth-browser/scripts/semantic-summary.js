/**
 * Semantic Summary Script (Inspired by Lightpanda Browser)
 * 
 * This script prunes the DOM and returns a token-efficient, 
 * AI-friendly semantic tree string.
 */

(function() {
    function isVisible(el) {
        if (!el.offsetParent && el.tagName !== 'BODY') return false;
        const style = window.getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden') return false;
        if (parseFloat(style.opacity) === 0) return false;
        return true;
    }

    function isInteractive(el) {
        const interactiveTags = ['A', 'BUTTON', 'INPUT', 'TEXTAREA', 'SELECT', 'DETAILS'];
        if (interactiveTags.includes(el.tagName)) return true;
        if (el.hasAttribute('onclick') || el.style.cursor === 'pointer' || el.hasAttribute('role') && ['button', 'link', 'checkbox', 'menuitem'].includes(el.getAttribute('role'))) return true;
        
        // Advanced: Check for added event listeners (hard in pure JS, but we can check common markers)
        if (el.classList.contains('btn') || el.classList.contains('button') || el.classList.contains('clickable')) return true;
        
        return false;
    }

    function getAriaName(el) {
        return el.getAttribute('aria-label') || el.getAttribute('title') || el.getAttribute('alt') || '';
    }

    function getSemanticRole(el) {
        const role = el.getAttribute('role');
        if (role) return role;
        
        const tagMap = {
            'A': 'link',
            'BUTTON': 'button',
            'H1': 'heading', 'H2': 'heading', 'H3': 'heading', 'H4': 'heading', 'H5': 'heading', 'H6': 'heading',
            'INPUT': 'input',
            'TEXTAREA': 'textbox',
            'SELECT': 'listbox',
            'NAV': 'navigation',
            'HEADER': 'banner',
            'FOOTER': 'contentinfo',
            'MAIN': 'main',
            'SECTION': 'region',
            'ARTICLE': 'article',
            'UL': 'list',
            'LI': 'listitem'
        };
        return tagMap[el.tagName] || 'generic';
    }

    const structuralRoles = ['none', 'generic', 'region', 'banner', 'navigation', 'main', 'list', 'listitem'];

    let nodeIdCounter = 0;
    const nodeMap = new Map();

    function walk(node, depth = 0) {
        if (node.nodeType === 1) { // Element
            if (!isVisible(node)) return null;
            if (['SCRIPT', 'STYLE', 'NOSCRIPT', 'SVG', 'HEAD'].includes(node.tagName)) return null;

            const role = getSemanticRole(node);
            const name = getAriaName(node);
            const interactive = isInteractive(node);
            const value = node.value || '';

            // Pruning Logic
            if (structuralRoles.includes(role) && !interactive && !name && !node.hasAttribute('id')) {
                // If it's just a structural wrapper with no unique ID or label, 
                // skip its entry but walk its children.
                let childrenText = '';
                for (const child of node.childNodes) {
                    const result = walk(child, depth);
                    if (result) childrenText += result;
                }
                return childrenText;
            }

            const nodeId = ++nodeIdCounter;
            nodeMap.set(nodeId, node);
            node.setAttribute('data-semantic-id', nodeId);

            let output = '  '.repeat(depth) + `[${nodeId}] ${role}`;
            if (name) output += ` '${name}'`;
            if (value) output += ` value='${value}'`;
            output += '\n';

            for (const child of node.childNodes) {
                const result = walk(child, depth + 1);
                if (result) output += result;
            }
            return output;

        } else if (node.nodeType === 3) { // Text
            const text = node.textContent.trim();
            if (text.length === 0) return null;
            
            // Avoid redundant nesting if parent already has this text as its "name"
            const parentName = node.parentElement ? getAriaName(node.parentElement) : '';
            if (parentName.includes(text)) return null;

            return '  '.repeat(depth) + `StaticText '${text}'\n`;
        }
        return null;
    }

    const result = walk(document.body);
    return result;
})();
