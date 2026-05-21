from dars.all import *
# pyrefly: ignore [missing-import]
from navbarcomp import create_navbar
# pyrefly: ignore [missing-import]
from footercomp import create_footer


roadmap = Page(
    create_navbar(),
    # Hero header section
    Container(
        Image(
            src="Dars-logo.png",
            alt="Dars Framework Logo",
            width="80px",
            height="80px",
            style={
                "margin-bottom": "16px",
                "filter": "drop-shadow(0 0 20px rgba(146, 255, 229, 0.3))",
            }
        ),
        Text(
            text="Development Roadmap",
            style={
                "font-size": "42px",
                "font-weight": "800",
                "margin": "0",
                "background": "linear-gradient(90deg, #92ffe5, #38c49f, #7dfdd8)",
                "background-clip": "text",
                "-webkit-background-clip": "text",
                "color": "transparent",
                "letter-spacing": "-0.5px",
            }
        ),
        Text(
            text="Track the journey from v1.9.6 to v2.0.0 — the complete production-grade fullstack Python framework.",
            style={
                "font-size": "17px",
                "color": "#a0cfc0",
                "max-width": "600px",
                "text-align": "center",
                "margin-top": "12px",
                "line-height": "1.6",
                "opacity": "0.85",
            }
        ),
        # Progress indicator
        Container(
            Container(
                id="roadmap-progress-fill",
                style={
                    "height": "100%",
                    "border-radius": "6px",
                    "background": "linear-gradient(90deg, #10b981, #38c49f, #92ffe5)",
                    "width": "0%",
                    "transition": "width 1.5s cubic-bezier(0.4, 0, 0.2, 1)",
                    "box-shadow": "0 0 12px rgba(16, 185, 129, 0.4)",
                }
            ),
            style={
                "width": "280px",
                "height": "8px",
                "background": "rgba(255,255,255,0.08)",
                "border-radius": "6px",
                "margin-top": "20px",
                "overflow": "hidden",
            }
        ),
        Text(
            text="0% complete",
            id="roadmap-progress-text",
            style={
                "font-size": "13px",
                "color": "rgba(160, 207, 192, 0.6)",
                "margin-top": "8px",
                "font-family": "monospace",
            }
        ),
        id="roadmap-hero",
        style={
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "justify-content": "center",
            "text-align": "center",
            "padding": "100px 20px 40px",
            "background": "linear-gradient(135deg, #0f1e1a 0%, #132d24 100%)",
            "border-bottom": "1px solid rgba(146, 255, 229, 0.08)",
        }
    ),
    # Markdown content
    Container(
        Container(
            Markdown(
                file_path="./roadmap/ROADMAP.md",
                dark_theme=True,
                class_name="markdown_docs"
            ),
            id="markdown-content-container",
            style={
                "max-width": "900px",
                "margin": "0 auto",
                "padding": "40px 24px 60px",
                "width": "100%",
            }
        ),
        id="markdown-layout",
        style={
            "min-height": "60vh",
            "background": "linear-gradient(180deg, #132d24 0%, #0f1e1a 100%)",
        }
    ),
    create_footer(),
    style="bg-[#0d1513]"
)

roadmap.add_script(
    dScript(code="""
(function() {
    var container = document.getElementById('markdown-content-container');
    if (!container) return;

    // ── Inject styles ──
    var style = document.createElement('style');
    style.textContent = `
        /* Checkboxes */
        .dars-checkbox {
            display: inline-flex; align-items: center; justify-content: center;
            width: 20px; height: 20px; border-radius: 5px; margin-right: 10px;
            flex-shrink: 0; vertical-align: middle; position: relative; top: 0px;
            transition: all 0.3s ease;
        }
        .dars-checkbox.checked {
            background: linear-gradient(135deg, #10b981, #059669);
            box-shadow: 0 0 10px rgba(16,185,129,0.3);
        }
        .dars-checkbox.checked::after {
            content: ""; display: block; width: 6px; height: 10px;
            border: solid #fff; border-width: 0 2.5px 2.5px 0;
            transform: rotate(45deg); margin-top: -2px;
        }
        .dars-checkbox.unchecked {
            background: rgba(255,255,255,0.04);
            border: 2px solid rgba(255,255,255,0.12);
        }
        .dars-cb-li {
            display: flex !important; align-items: flex-start;
            list-style: none !important; padding: 4px 0;
        }
        .dars-cb-li::before { display: none !important; }

        /* Section cards */
        #markdown-content-container h3 {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(146, 255, 229, 0.08);
            border-radius: 10px;
            padding: 14px 20px;
            margin-top: 32px;
            margin-bottom: 16px;
            font-size: 18px;
            position: relative;
            overflow: hidden;
        }
        #markdown-content-container h3::before {
            content: "";
            position: absolute; left: 0; top: 0; bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, #10b981, #059669);
            border-radius: 3px 0 0 3px;
        }

        /* Tables */
        #markdown-content-container table {
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(146, 255, 229, 0.1);
            width: 100%;
        }
        #markdown-content-container th {
            background: rgba(16, 185, 129, 0.12) !important;
            border-bottom: 1px solid rgba(146, 255, 229, 0.15) !important;
            padding: 12px 16px !important;
            font-weight: 600;
            text-align: left;
        }
        #markdown-content-container td {
            padding: 10px 16px !important;
            border-bottom: 1px solid rgba(255,255,255,0.04) !important;
        }
        #markdown-content-container tr:last-child td {
            border-bottom: none !important;
        }

        /* HR dividers */
        #markdown-content-container hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(146,255,229,0.15), transparent);
            margin: 36px 0;
        }

        /* Completed section */
        #markdown-content-container h2 {
            font-size: 22px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(146, 255, 229, 0.1);
            margin-top: 40px;
        }
    `;
    document.head.appendChild(style);

    // ── Transform checkboxes ──
    var total = 0, checked = 0;
    var items = container.querySelectorAll('li');
    for (var i = 0; i < items.length; i++) {
        var li = items[i];
        var text = li.textContent;
        if (/^\\s*\\[[ x]\\]/.test(text)) {
            total++;
            var isChecked = /^\\s*\\[x\\]/i.test(text);
            if (isChecked) checked++;
            var cls = isChecked ? 'checked' : 'unchecked';
            var span = '<span class="dars-checkbox ' + cls + '"></span>';
            li.innerHTML = li.innerHTML.replace(/\\[[ x]\\]\\s*/, '');
            li.insertAdjacentHTML('afterbegin', span);
            li.classList.add('dars-cb-li');
        }
    }

    // ── Update progress bar ──
    if (total > 0) {
        var pct = Math.round((checked / total) * 100);
        var fill = document.getElementById('roadmap-progress-fill');
        var txt = document.getElementById('roadmap-progress-text');
        if (fill) {
            setTimeout(function() { fill.style.width = pct + '%'; }, 300);
        }
        if (txt) {
            txt.textContent = checked + ' / ' + total + ' tasks (' + pct + '%)';
        }
    }
})();
""")
)