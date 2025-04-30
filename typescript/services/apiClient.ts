export interface ApiClientOptions {
    baseUrl: string;
    apiKey: string;
    timeout?: number;
  }
  
  export class StandardApiClient {
    protected baseUrl: string;
    protected apiKey: string;
    protected timeout: number;
  
    constructor(options: ApiClientOptions) {
      this.baseUrl = options.baseUrl;
      this.apiKey = options.apiKey;
      this.timeout = options.timeout || 5000;
      console.log(`[INFO] StandardApiClient for ${this.baseUrl} initialized. Timeout: ${this.timeout}ms. Key: ${this.apiKey.substring(0,4)}...`);
    }
  
    async get<T>(endpoint: string): Promise<T> {
      const response = await fetch(`<span class="math-inline">\{this\.baseUrl\}</span>{endpoint}`, { // Corrigido para não ter dupla '/'
        headers: {
          'X-Api-Key': this.apiKey,
          'X-Custom-Header': 'ValorPadraoEmpresa',
          'Content-Type': 'application/json'
        },
      });
      if (!response.ok) {
        const errorBody = await response.text();
        console.error(`[ERROR] API GET <span class="math-inline">\{this\.baseUrl\}</span>{endpoint} failed: ${response.status} - ${response.statusText}. Body: ${errorBody}`);
        throw new Error(`API Error (${response.status}) accessing ${endpoint}: ${response.statusText} - PadraoEmpresa`); // Regra de Negócio
      }
      return response.json() as T;
    }
  
    async post<T, U>(endpoint: string, data: T): Promise<U> {
      const response = await fetch(`<span class="math-inline">\{this\.baseUrl\}</span>{endpoint}`, { // Corrigido
        method: 'POST',
        headers: {
          'X-Api-Key': this.apiKey,
          'X-Custom-Header': 'ValorPadraoEmpresa',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        const errorBody = await response.text();
        console.error(`[ERROR] API POST <span class="math-inline">\{this\.baseUrl\}</span>{endpoint} failed: ${response.status} - ${response.statusText}. Body: ${errorBody}`);
        throw new Error(`API Error POST (${response.status}) accessing ${endpoint}: ${response.statusText} - PadraoEmpresa`);
      }
      return response.json() as U;
    }
  }