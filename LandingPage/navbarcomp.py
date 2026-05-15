from dars.all import *
from dars.env import DarsEnv

def create_navbar():
    left_block = Container(
        Image(
            alt="Logo",
            src="Dars-logo.png",
            width="38px",
            height="38px",
            style="object-contain mr-[10px]"
        ),
        Text(
            text="Dars Framework",
            style="fs-[20px] font-bold text-[#a2ffe2] m-[0]"
        ),
        id="navbar-left",
        style="flex items-center justify-start h-full"
    )

    # Botones para la parte derecha del navbar (desktop)
    right_block = Container(
        Link(
            "Home",
            href="/" if DarsEnv.dev else "https://ztamdev.github.io/Dars-Framework/",
            style="text-[#a0cfc0] no-underline margin-[0_15px] font-medium fs-[16px] transition-all duration-300 ease-in-out padding-[8px_16px] rounded-[6px]"
        ),
        Link(
            "Documentation",
            href="/docs.html" if DarsEnv.dev else "https://ztamdev.github.io/Dars-Framework/docs.html",
            style="text-[#a0cfc0] no-underline margin-[0_15px] font-medium fs-[16px] transition-all duration-300 ease-in-out padding-[8px_16px] rounded-[6px]"
        ),
        Link(
            "Releases",
            href="/releases.html" if DarsEnv.dev else "https://ztamdev.github.io/Dars-Framework/releases.html",
            style="text-[#a0cfc0] no-underline margin-[0_15px] font-medium fs-[16px] transition-all duration-300 ease-in-out padding-[8px_16px] rounded-[6px]"
        ),
        Link(
            "Roadmap",
            href="/roadmap.html" if DarsEnv.dev else "https://ztamdev.github.io/Dars-Framework/roadmap.html",
            style="text-[#a0cfc0] no-underline margin-[0_15px] font-medium fs-[16px] transition-all duration-300 ease-in-out padding-[8px_16px] rounded-[6px]"
        ),
        Link(
            "PlayGround",
            href="https://dars-playground.vercel.app/",
            style="text-[#a0cfc0] no-underline margin-[0_15px] font-medium fs-[16px] transition-all duration-300 ease-in-out padding-[8px_16px] rounded-[6px]"
        ),
        Link(
            "GitHub",
            href="https://github.com/ZtaMDev/Dars-Framework",
            style="text-[#a0cfc0] no-underline margin-[0_15px] font-medium fs-[16px] transition-all duration-300 ease-in-out padding-[8px_16px] rounded-[6px]"
        ),
        id="navbar-right",
        style="flex items-center justify-end h-full"
    )

    # Menú hamburguesa mejorado para móviles
    hamburger_menu = Container(
        # Botón hamburguesa mejorado
        Container(
            Container(
                Container(style="w-[24px] h-[2px] bg-[#a2ffe2] rounded-[2px] transition-all duration-300 ease-in-out margin-[3px_0]"),
                Container(style="w-[24px] h-[2px] bg-[#a2ffe2] rounded-[2px] transition-all duration-300 ease-in-out margin-[3px_0]"),
                Container(style="w-[18px] h-[2px] bg-[#a2ffe2] rounded-[2px] transition-all duration-300 ease-in-out margin-[3px_0]"),
                style="flex flex-col items-center justify-center w-[44px] h-[44px] relative"
            ),
            id="hamburger-btn",
            style="hidden bg-[rgba(162,_255,_226,_0.1)] border-1 border-solid border-[rgba(162,_255,_226,_0.3)] rounded-[10px] cursor-pointer p-[0] z-1000 transition-all duration-300 ease-in-out items-center justify-center backdrop-filter-[blur(10px)] box-shadow-[0_4px_15px_rgba(0,0,0,0.2)]"
        ),
        
        # Menú desplegable
        Container(
            Link(
                "Home",
                href="/" if DarsEnv.dev else "https://ztamdev.github.io/Dars-Framework/",
                style="block text-[#a0cfc0] no-underline padding-[18px_25px] font-medium fs-[18px] transition-all duration-300 ease-in-out border-bottom-[1px_solid_rgba(100,_255,_200,_0.1)]"
            ),
            Link(
                "Documentation",
                href="/docs.html" if DarsEnv.dev else "https://ztamdev.github.io/Dars-Framework/docs.html",
                style="block text-[#a0cfc0] no-underline padding-[18px_25px] font-medium fs-[18px] transition-all duration-300 ease-in-out border-bottom-[1px_solid_rgba(100,_255,_200,_0.1)]"
            ),
            Link(
                "Releases",
                href="/releases.html" if DarsEnv.dev else "https://ztamdev.github.io/Dars-Framework/releases.html",
                style="block text-[#a0cfc0] no-underline padding-[18px_25px] font-medium fs-[18px] transition-all duration-300 ease-in-out border-bottom-[1px_solid_rgba(100,_255,_200,_0.1)]"
            ),
            Link(
                "PlayGround",
                href="https://dars-playground.vercel.app/",
                style="block text-[#a0cfc0] no-underline padding-[18px_25px] font-medium fs-[18px] transition-all duration-300 ease-in-out border-bottom-[1px_solid_rgba(100,_255,_200,_0.1)]"
            ),
            Link(
                "GitHub",
                href="https://github.com/ZtaMDev/Dars-Framework",
                style="block text-[#a0cfc0] no-underline padding-[18px_25px] font-medium fs-[18px] transition-all duration-300 ease-in-out"
            ),
            id="mobile-menu",
            style="hidden fixed top-[64px] left-[0] w-full bg-[rgba(15,_25,_22,_0.98)] backdrop-filter-[blur(25px)] border-top-[1px_solid_rgba(100,_255,_200,_0.15)] box-shadow-[0_8px_30px_rgba(0,0,0,0.4)] z-999 flex-col"
        ),
        id="hamburger-menu",
        style="hidden items-center justify-end h-full"
    )

    return Container(
        Navbar(
            left_block,
            Container(
                right_block,
                hamburger_menu,
                style="flex items-center justify-end h-full gap-[15px]"
            ),
            id="dars-navbar",
            style="flex items-center justify-between h-[64px] padding-[0_40px] fixed top-[0] w-full z-999 backdrop-filter-[blur(12px)] bg-[rgba(20,_30,_27,_0.6)] border-bottom-[1px_solid_rgba(100,_255,_200,_0.1)] box-shadow-[0_2px_10px_rgba(0,0,0,0.2)]"
        ),
    )