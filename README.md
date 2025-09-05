# Repositório Base de Demonstração para Gemini Code Assist (gcae-demo)

Este repositório serve como uma base de código de exemplo, demonstrando padrões comuns, funcionalidades e regras de negócio que podem ser utilizados para treinar, guiar e demonstrar as capacidades do Gemini Code Assist. O código está organizado em Python, TypeScript, JavaScript e Terraform (focado em recursos GCP).

## Visão Geral

O objetivo principal é fornecer exemplos claros de como estruturar código e definir recursos de infraestrutura, incorporando regras de negócio específicas que o Gemini pode aprender e ajudar a replicar ou estender.

## Como Utilizar

Este repositório pode ser usado como:
1.  **Referência:** Para entender como implementar padrões e regras de negócio específicas.
2.  **Base para Demonstrações:** Para mostrar como o Gemini Code Assist pode ajudar a gerar código que adere a estas convenções.
3.  **Fonte de Contexto:** Trechos deste código podem ser fornecidos ao Gemini como contexto para gerar novo código que siga os mesmos padrões.

Ao demonstrar o Gemini Code Assist, pode-se pedir para:
* Começar a desenvolver código correlato e esperar completude semelhante.
* Conectar tools para interação.
* Criar um novo tipo de cliente de API seguindo o padrão `StandardApiClient`.
* Implementar uma nova lógica de validação aderente às regras de `validation.ts`.
* Gerar um novo módulo Terraform para um recurso GCP diferente, mas mantendo as convenções de nomenclatura e labels.
* Adicionar um novo tipo de desconto na `discountCalculator.js` mantendo o formato de log.
