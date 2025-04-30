function logStandardError(errorMessage, errorCode = 'GENERAL_ERROR', details = {}) {
    const timestamp = new Date().toISOString();
    const errorPayload = {
        timestamp,
        level: 'ERROR',
        serviceContext: 'GeminiDemoBaseRepo',
        traceId: `trace_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`, // Regra de Negócio
        errorCode,
        message: errorMessage,
        details,
    };
    console.error(JSON.stringify(errorPayload, null, 2));
    return errorPayload;
}
module.exports = { logStandardError };