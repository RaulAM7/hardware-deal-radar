# 00 — Product Vision

## Producto

**Hardware Deal Radar** es una herramienta interna para detectar oportunidades de compra de hardware profesional usado/reacondicionado, empezando por portátiles ThinkPad en eBay Europa.

El sistema debe observar búsquedas configuradas, normalizar resultados, estimar coste total, puntuar oportunidades y avisar únicamente cuando haya algo que merezca atención.

## Problema

El usuario necesita valorar la sustitución de su portátil actual por un equipo claramente superior para desarrollo intensivo con IA y multitarea pesada.

La opción Apple MacBook Air dejó de ser tan atractiva por la subida reciente de precios y por el salto insuficiente entre 16 GB actuales y 24 GB de memoria unificada si el objetivo es trabajar con muchas sesiones de Codex/Claude Code, worktrees, navegador, servicios locales, contenedores y herramientas de productividad simultáneas.

El mercado de portátiles business usados/reacondicionados puede tener ineficiencias reales, especialmente cuando empresas renuevan flotas y liquidan equipos amortizados. En ese contexto, ThinkPad y portátiles business equivalentes pueden aparecer a precios muy interesantes, pero las oportunidades son esporádicas y requieren vigilancia.

## Oportunidad

Construir un radar propio permite:

- detectar oportunidades antes de que desaparezcan;
- comparar marketplaces europeos;
- penalizar costes ocultos como aduanas o teclado extranjero;
- evitar falsas gangas;
- concentrar la atención solo en alertas accionables;
- crear una herramienta reutilizable para futuras compras de hardware;
- entrenar una metodología agentic B-shot aplicable a otros proyectos de Skilland/Edukami.

## Doble naturaleza del proyecto

Este proyecto no es solo un radar de compras.

Es también un experimento metodológico:

1. Diseñar un producto pequeño, útil y cerrado.
2. Formalizar decisiones estratégicas y técnicas en documentos de contexto.
3. Lanzar un primer `/goal` para generar specs absurdamente detalladas.
4. Lanzar un segundo `/goal` para implementar el sistema completo.

El éxito metodológico importa tanto como el éxito funcional.

## Principio rector

Codex no debe decidir el producto.

Codex debe convertir decisiones ya cerradas en specs e implementación.

Las decisiones de producto, alcance y arquitectura deben estar tomadas antes de ejecutar los goals.
