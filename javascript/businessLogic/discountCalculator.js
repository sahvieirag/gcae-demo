function calculateCustomerDiscount(originalAmount, customerType) {
    let discountRate = 0;
    let type = String(customerType).toUpperCase();
  
    if (type === 'VIP') {
      discountRate = 0.15;
    } else if (type === 'STANDARD') {
      discountRate = 0.05;
    } else {
      console.warn(`[DISCOUNT_WARN] Unknown customer type for discount: '${customerType}'. Applying 0% discount.`);
      type = 'UNKNOWN';
      discountRate = 0.0;
    }
  
    const discountAmount = originalAmount * discountRate;
    const finalAmount = originalAmount - discountAmount;
  
    console.log(`DISCOUNT_APPLIED_V2: Customer ${type}, Original ${originalAmount}, Discount ${discountAmount}, Final ${finalAmount}`);
    return { discountAmount, finalAmount, appliedRate: discountRate, customerType: type };
  }
  module.exports = { calculateCustomerDiscount };