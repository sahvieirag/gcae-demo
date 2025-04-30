# Repositório Base de Demonstração para Gemini Code Assist (gcae-demo)

Este repositório serve como uma base de código de exemplo, demonstrando padrões comuns, funcionalidades e regras de negócio que podem ser utilizados para treinar, guiar e demonstrar as capacidades do Gemini Code Assist. O código está organizado em TypeScript, JavaScript e Terraform (focado em recursos GCP).

## Visão Geral

O objetivo principal é fornecer exemplos claros de como estruturar código e definir recursos de infraestrutura, incorporando regras de negócio específicas que o Gemini pode aprender e ajudar a replicar ou estender.

## Módulos e Funcionalidades

### 1. TypeScript (`./typescript`)

#### a. Cliente de API Padrão (`./typescript/services/apiClient.ts`)

* **Funcionalidade:**
    * Define uma classe `StandardApiClient` reutilizável para realizar chamadas HTTP (GET, POST) a APIs externas.
    * Padroniza a inicialização do cliente, configuração de headers e tratamento de erros.
* **Regras de Negócio & Convenções:**
    * **Construtor e Inicialização:**
        * Requer `baseUrl` e `apiKey` como opções.
        * `timeout` opcional, com padrão de `5000ms`.
        * **Log de Inicialização Específico:** Ao ser instanciado, loga uma mensagem formatada: `[INFO] StandardApiClient for ${this.baseUrl} initialized. Timeout: ${this.timeout}ms. Key: ${this.apiKey.substring(0,4)}...` (mascarando parte da API Key).
    * **Headers Padrão:**
        * Todas as requisições incluem automaticamente o header `X-Api-Key` com o valor fornecido no construtor.
        * Todas as requisições incluem automaticamente o header customizado `X-Custom-Header: 'ValorPadraoEmpresa'`.
        * `Content-Type: 'application/json'` é definido para todas as requisições.
    * **Tratamento de Erro Padronizado:**
        * Em caso de resposta não-OK (status >= 400), um erro é lançado.
        * A mensagem de erro segue o formato: `API Error (${response.status}) accessing ${endpoint}: ${response.statusText} - PadraoEmpresa`. (Ex: `API Error (404) accessing /users/123: Not Found - PadraoEmpresa`).
        * Antes de lançar o erro, detalhes da falha (status, statusText, response body) são logados no console com o prefixo `[ERROR]`.

#### b. Utilitários de Validação (`./typescript/utils/validation.ts`)

* **Funcionalidade:**
    * Fornece funções para validar IDs de usuário (`isValidUserId`) e gerar IDs padronizados (`generateStandardId`).
* **Regras de Negócio & Convenções:**
    * **Formato de ID de Usuário:**
        * IDs de usuário devem obrigatoriamente começar com o prefixo definido em `USER_ID_PREFIX` (atualmente `"usr_"`).
        * IDs de usuário devem ter um comprimento mínimo de caracteres *após* o prefixo, definido por `ID_MIN_LENGTH_AFTER_PREFIX` (atualmente `8`).
    * **Logging de Validação:**
        * Se um ID é inválido, uma mensagem de aviso é logada: `[VALIDATION_FAIL] Invalid User ID format: ${id}. Must start with ${USER_ID_PREFIX} and have at least ${ID_MIN_LENGTH_AFTER_PREFIX} chars after prefix.`
        * Se um ID é válido, uma mensagem de sucesso é logada: `[VALIDATION_PASS] User ID format valid: ${id}`.
    * **Logging de Geração de ID:**
        * A função `generateStandardId` loga o ID gerado: `[ID_FACTORY] Generated ID: ${result} with prefix ${prefix}`.

### 2. JavaScript (`./javascript`)

#### a. Lógica de Negócio - Calculadora de Descontos (`./javascript/businessLogic/discountCalculator.js`)

* **Funcionalidade:**
    * Calcula o desconto aplicável a um cliente com base no seu tipo e no valor original.
    * Loga a transação de desconto.
* **Regras de Negócio & Convenções:**
    * **Taxas de Desconto por Tipo de Cliente:**
        * `VIP`: 15% de desconto.
        * `STANDARD`: 5% de desconto.
        * `NONE`: 0% de desconto.
        * Tipos desconhecidos: 0% de desconto e um aviso é logado (`[DISCOUNT_WARN] Unknown customer type for discount: '${customerType}'. Applying 0% discount.`).
    * **Normalização do Tipo de Cliente:** O `customerType` é convertido para maiúsculas para garantir a correspondência insensível a caixa.
    * **Formato de Log Específico (V2):**
        * Toda aplicação de desconto é logada no formato: `DISCOUNT_APPLIED_V2: Customer ${type}, Original ${originalAmount}, Discount ${discountAmount}, Final ${finalAmount}`.
    * **Valor de Retorno:** A função retorna um objeto contendo `discountAmount`, `finalAmount`, `appliedRate`, e `customerType` (normalizado).

#### b. Utilitários - Tratador de Erros (`./javascript/utils/errorHandler.js`)

* **Funcionalidade:**
    * Fornece uma função `logStandardError` para garantir um formato de log de erro consistente em aplicações JavaScript.
* **Regras de Negócio & Convenções:**
    * **Formato de Log JSON:** Erros são logados como uma string JSON.
    * **Campos Padrão no Log de Erro:**
        * `timestamp`: Data e hora do erro no formato ISO.
        * `level`: Fixo como `'ERROR'`.
        * `serviceContext`: Fixo como `'GeminiDemoBaseRepo'` (identifica a origem do padrão de log).
        * `traceId`: Um ID de rastreamento único gerado no formato `trace_${Date.now()}_${random_string}`.
        * `errorCode`: Código de erro fornecido (padrão: `'GENERAL_ERROR'`).
        * `message`: A mensagem de erro principal.
        * `details`: Um objeto contendo quaisquer detalhes estruturados adicionais sobre o erro.

### 3. Terraform (`./terraform/modules`)

#### a. Módulo GCP: Standard Storage Bucket (`./terraform/modules/gcp_standard_bucket`)

* **Funcionalidade:**
    * Módulo Terraform para criar e configurar Google Cloud Storage buckets de forma padronizada.
* **Regras de Negócio & Convenções:**
    * **Convenção de Nomenclatura:** Nome do bucket é `${var.bucket_name_prefix}-bucket-${var.env_suffix}-${random_id.bucket_suffix.hex}`.
    * **Localização Padrão:** `var.location` assume `US-CENTRAL1` se não especificado.
    * **Versionamento:** Habilitado por padrão (`versioning { enabled = true }`).
    * **Classe de Armazenamento Padrão:** `STANDARD`.
    * **Acesso Uniforme em Nível de Bucket:** Habilitado (`uniform_bucket_level_access = true`).
    * **Labels Obrigatórias:**
        * `environment`: Valor de `var.env_suffix`.
        * `managed_by`: Fixo como `"terraform-gemini-base"`.
        * `cost_allocation_code`: Fixo como `"it-infra-001"`.
        * `data_classification`: Valor de `var.data_classification_label` (padrão: `"general"`).
    * **Ciclo de Vida:** Configurado com `prevent_destroy = true` para evitar exclusões acidentais (especialmente para ambientes não-dev).

#### b. Módulo GCP: Standard Compute VM (`./terraform/modules/gcp_standard_vm`)

* **Funcionalidade:**
    * Módulo Terraform para criar e configurar instâncias Google Compute Engine (VM) de forma padronizada.
* **Regras de Negócio & Convenções:**
    * **Convenção de Nomenclatura:** Nome da VM é `${var.vm_name_prefix}-${var.env}-${random_id.vm_suffix.hex}`.
    * **Zona Padrão:** `var.zone` assume `us-central1-a` se não especificado.
    * **Tipo de Máquina Padrão:** `var.machine_type` assume `e2-medium` se não especificado.
    * **Imagem de Boot Padrão:** `var.boot_disk_image` assume `debian-cloud/debian-11` se não especificado.
    * **Labels Obrigatórias:**
        * `environment`: Valor de `var.env`.
        * `managed_by`: Fixo como `"terraform-gemini-base"`.
        * `cost_center`: Fixo como `"cc123-department-x"`.
        * `app_name`: Valor de `var.vm_name_prefix`.
    * **Conta de Serviço:** Utiliza uma conta de serviço com escopo `cloud-platform`.
    * **Configuração de Rede:** Assume a rede VPC `"default"`.
    * **Atualizações:** Configurado com `allow_stopping_for_update = true`.

## Como Utilizar

Este repositório pode ser usado como:
1.  **Referência:** Para entender como implementar padrões e regras de negócio específicas.
2.  **Base para Demonstrações:** Para mostrar como o Gemini Code Assist pode ajudar a gerar código que adere a estas convenções.
3.  **Fonte de Contexto:** Trechos deste código podem ser fornecidos ao Gemini como contexto para gerar novo código que siga os mesmos padrões.

Ao demonstrar o Gemini Code Assist, pode-se pedir para:
* Criar um novo tipo de cliente de API seguindo o padrão `StandardApiClient`.
* Implementar uma nova lógica de validação aderente às regras de `validation.ts`.
* Gerar um novo módulo Terraform para um recurso GCP diferente, mas mantendo as convenções de nomenclatura e labels.
* Adicionar um novo tipo de desconto na `discountCalculator.js` mantendo o formato de log.
