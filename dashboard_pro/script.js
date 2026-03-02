
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('nav a');
    const sections = document.querySelectorAll('section');
    const header = document.querySelector('header');
    const exploreBtn = document.getElementById('explore-btn');
    const logoBtn = document.getElementById('logo-btn');

    // Manejar estilo del header en scroll
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) header.classList.add('scrolled');
        else header.classList.remove('scrolled');
    });

    let isAnimating = false;

    // Función para cambiar de sección SPA
    function navigateTo(targetId) {
        if (isAnimating) return;

        const currentActive = document.querySelector('section.active');
        const targetSection = document.getElementById(targetId);

        if (!targetSection || (currentActive && currentActive.id === targetId)) return;

        isAnimating = true;

        navLinks.forEach(link => link.classList.remove('active'));
        const activeLink = document.querySelector(`nav a[data-target="${targetId}"]`);
        if (activeLink) activeLink.classList.add('active');

        if (currentActive) {
            currentActive.classList.add('slide-out');
            currentActive.classList.remove('animation-done');
            setTimeout(() => {
                currentActive.classList.remove('active', 'slide-out');
                window.scrollTo(0, 0);
                targetSection.classList.add('active');
                window.dispatchEvent(new Event('resize'));
                setTimeout(() => {
                    isAnimating = false;
                    targetSection.classList.add('animation-done');
                }, 600);
            }, 380);
        } else {
            targetSection.classList.add('active');
            window.dispatchEvent(new Event('resize'));
            setTimeout(() => { targetSection.classList.add('animation-done'); }, 600);
            isAnimating = false;
        }
    }

    // Event listeners para la navegación
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('data-target');
            navigateTo(target);
        });
    });

    exploreBtn.addEventListener('click', () => navigateTo('eda'));
    logoBtn.addEventListener('click', () => navigateTo('home'));

    // Next buttons
    document.querySelectorAll('.next-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo(btn.closest('.next-btn').getAttribute('data-target'));
        });
    });

    // Prev buttons
    document.querySelectorAll('.prev-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo(btn.closest('.prev-btn').getAttribute('data-target'));
        });
    });

    // --- NAVEGACIÓN CON TECLADO ---
    const sectionsOrder = ['home', 'eda', 'modelo', 'resultados', 'estrategia'];

    document.addEventListener('keydown', (e) => {
        if (isAnimating) return;
        const currentActive = document.querySelector('section.active');
        if (!currentActive) return;

        let currentIndex = sectionsOrder.indexOf(currentActive.id);

        if (e.key === 'ArrowRight') {
            if (currentIndex < sectionsOrder.length - 1) {
                navigateTo(sectionsOrder[currentIndex + 1]);
            }
        } else if (e.key === 'ArrowLeft') {
            if (currentIndex > 0) {
                navigateTo(sectionsOrder[currentIndex - 1]);
            }
        }
    });

    // --- ANIMACIÓN CANVAS DE SISMOS Y CLUSTERS ---
    function initSeismicCanvas() {
        const canvas = document.getElementById('seismic-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let width, height;

        function resizeCanvas() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        const nodes = [];
        const numNodes = 100; // Número de "sismos" en la pantalla
        const maxDist = 180;  // Distancia para formar "fallas" (clusters)

        // Colores que machean con los 5 clústers (rojo, verde, amarillo, azul, naranja)
        const colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231'];

        for (let i = 0; i < numNodes; i++) {
            nodes.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 1.2,
                vy: (Math.random() - 0.5) * 1.2,
                radius: Math.random() * 2 + 1.5,
                color: colors[Math.floor(Math.random() * colors.length)],
                pulse: Math.random() * Math.PI * 2,
                ringTimer: Math.random() * 300,
                rings: []
            });
        }

        function drawCanvas() {
            // Fondo oscuro semitransparente para efecto de estela
            ctx.fillStyle = 'rgba(15, 23, 42, 0.4)';
            ctx.fillRect(0, 0, width, height);

            for (let i = 0; i < nodes.length; i++) {
                let n = nodes[i];
                n.x += n.vx;
                n.y += n.vy;

                // Rebote en bordes
                if (n.x < 0 || n.x > width) n.vx *= -1;
                if (n.y < 0 || n.y > height) n.vy *= -1;

                // Ocasionalmente generar "onda sísmica"
                n.ringTimer--;
                if (n.ringTimer <= 0) {
                    n.rings.push({ r: n.radius, alpha: 1 });
                    n.ringTimer = 100 + Math.random() * 400; // Siguiente onda
                }

                // Dibujar y expandir ondas sísmicas
                for (let j = n.rings.length - 1; j >= 0; j--) {
                    let ring = n.rings[j];
                    ring.r += 0.8;
                    ring.alpha -= 0.012;
                    if (ring.alpha <= 0) {
                        n.rings.splice(j, 1);
                        continue;
                    }
                    ctx.beginPath();
                    ctx.arc(n.x, n.y, ring.r, 0, Math.PI * 2);
                    ctx.strokeStyle = `rgba(255, 255, 255, ${ring.alpha * 0.3})`;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }

                // Conexiones de clúster (rayos entre nodos cercanos)
                for (let j = i + 1; j < nodes.length; j++) {
                    let n2 = nodes[j];
                    let dx = n.x - n2.x;
                    let dy = n.y - n2.y;
                    let dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < maxDist) {
                        ctx.beginPath();
                        ctx.moveTo(n.x, n.y);
                        ctx.lineTo(n2.x, n2.y);
                        // Líneas sutiles de conexión simulando fallas tectónicas
                        ctx.strokeStyle = `rgba(180, 200, 255, ${(1 - dist / maxDist) * 0.25})`;
                        ctx.lineWidth = 0.8;
                        ctx.stroke();
                    }
                }

                // Dibujar epicentro (el punto)
                ctx.beginPath();
                ctx.arc(n.x, n.y, n.radius + Math.sin(n.pulse), 0, Math.PI * 2);
                ctx.fillStyle = n.color;
                ctx.fill();
                n.pulse += 0.08;
            }
            requestAnimationFrame(drawCanvas);
        }
        drawCanvas();
    }

    initSeismicCanvas();

});
