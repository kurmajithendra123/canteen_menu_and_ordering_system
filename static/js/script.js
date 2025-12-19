let cart = {};
let menuItems = [];

document.addEventListener('DOMContentLoaded', () => {
    fetchMenu();
    setupEventListeners();
});

async function fetchMenu() {
    try {
        let url = '/api/menu';
        // Check window.CURRENT_CANTEEN
        if (window.CURRENT_CANTEEN) {
            url += `?canteen=${encodeURIComponent(window.CURRENT_CANTEEN)}`;
            console.log("Fetching menu for:", window.CURRENT_CANTEEN);
        } else {
            console.log("Fetching full menu (no canteen selected)");
        }

        console.log("Fetching URL:", url);
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        menuItems = await response.json();
        console.log("Menu items loaded:", menuItems.length);

        if (menuItems.length === 0) {
            document.getElementById('menu-grid').innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No items found for this canteen.</p>';
            return;
        }

        renderMenu(menuItems);
    } catch (error) {
        console.error('Error fetching menu:', error);
        document.getElementById('menu-grid').innerHTML = `<p style="color: red; grid-column: 1/-1; text-align: center;">Error loading menu: ${error.message}</p>`;
        // Alert for visibility since user says "menu not showing"
        // alert("Failed to load menu: " + error.message); 
    }
}

function renderMenu(items) {
    const grid = document.getElementById('menu-grid');
    grid.innerHTML = items.map(item => `
        <div class="menu-card animate-fade-in">
            <img src="${item.image_url}" alt="${item.name}" class="card-img">
            <div class="card-content">
                <span class="card-category">${item.category}</span>
                <h3 class="card-title">${item.name}</h3>
                <div class="card-footer" id="item-footer-${item.id}">
                    <span class="price">₹${item.price}</span>
                    ${renderItemButton(item)}
                </div>
            </div>
        </div>
    `).join('');
}

function renderItemButton(item) {
    const cartItem = cart[item.id];
    if (cartItem) {
        return `
            <div class="qty-control-card">
                <button onclick="removeFromCart(${item.id})">-</button>
                <span>${cartItem.quantity}</span>
                <button onclick="addToCart(${item.id})">+</button>
            </div>
        `;
    } else {
        return `<button onclick="addToCart(${item.id})" class="add-btn">ADD</button>`;
    }
}

window.addToCart = function (id) {
    if (cart[id]) {
        cart[id].quantity++;
    } else {
        const item = menuItems.find(i => i.id === id);
        cart[id] = { ...item, quantity: 1 };
    }
    updateCartUI();
    updateCardUI(id); // New function to update specifically the card
    // showToast remove or keep? Maybe remove since visual feedback is strong now
};

window.removeFromCart = function (id) {
    if (cart[id]) {
        cart[id].quantity--;
        if (cart[id].quantity <= 0) {
            delete cart[id];
        }
    }
    updateCartUI();
    updateCardUI(id);
};

function updateCardUI(id) {
    // Find item
    const item = menuItems.find(i => i.id === id);
    if (!item) return;

    // Find footer element
    const footer = document.getElementById(`item-footer-${id}`);
    if (footer) {
        // Re-render just the button part? 
        // Or simpler: replace the innerHTML of the container's button Area
        // Easier: Re-render the "price + button" combo or just make a dedicated container for button
        // Let's stick to replacing the whole footer content or just finding the button container.
        // Actually, my renderItemButton returns the HTML. I can just replace the button part.

        // But the footer has price too. Let's rebuild the footer HTML.
        footer.innerHTML = `
            <span class="price">₹${item.price}</span>
            ${renderItemButton(item)}
        `;
    }
}

function updateCartUI() {
    const cartCount = Object.values(cart).reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('cart-count').innerText = cartCount;

    // Calculate totals first
    let itemTotal = 0;
    Object.values(cart).forEach(item => {
        itemTotal += item.price * item.quantity;
    });

    const tax = itemTotal * 0.05; // 5% GST
    const platformFee = Object.keys(cart).length > 0 ? 2.00 : 0;
    const finalTotal = itemTotal + tax + platformFee;


    // Floating Cart Bar logic REMOVED

    const cartItemsContainer = document.getElementById('cart-items-container');

    if (Object.keys(cart).length === 0) {
        cartItemsContainer.innerHTML = `
            <div style="text-align: center; padding: 3rem 1rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🍽️</div>
                <h3 style="color: var(--text-main);">Good food is always cooking</h3>
                <p style="color: var(--text-muted);">Your cart is empty. Add something from the menu!</p>
            </div>`;
        document.getElementById('cart-total-amount').innerText = "0.00";
        // Also update the button amount
        const finalPaySpan = document.getElementById('final-pay-amount');
        if (finalPaySpan) finalPaySpan.innerText = "0.00";
        return;
    }

    // 1. Items List
    let itemsHtml = Object.values(cart).map(item => {
        // Mock Veg/Non-veg based on keyword
        const isNonVeg = item.name.toLowerCase().includes('chicken') || item.name.toLowerCase().includes('egg');
        const iconClass = isNonVeg ? 'veg-icon non-veg-icon' : 'veg-icon';

        return `
            <div class="cart-item-modern">
                <div style="display: flex; align-items: center;">
                    <div class="${iconClass}"></div>
                    <div>
                        <div style="font-weight: 500;">${item.name}</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">₹${item.price}</div>
                    </div>
                </div>
                
                <div class="cart-controls" style="background: white; border: 1px solid #d1d5db;">
                    <button class="qty-btn" onclick="removeFromCart(${item.id})">-</button>
                    <span style="font-weight: 600; color: #16a34a;">${item.quantity}</span>
                    <button class="qty-btn" onclick="addToCart(${item.id})">+</button>
                </div>

                <div style="text-align: right; font-weight: 500;">
                    ₹${item.price * item.quantity}
                </div>
            </div>
        `;
    }).join('');

    // 2. Cancellation / Info Banner
    const infoBanner = `
        <div class="cancellation-policy">
            <div style="font-size: 1.2rem;">💬</div>
            <div>
                <strong>Avoid cancellation</strong><br>
                Please ensure you are at the correct canteen before placing the order.
            </div>
        </div>
    `;

    // 3. Bill Details
    // (Variables tax, platformFee, finalTotal are calculated at start of function)

    const billDetails = `
        <div class="bill-details">
            <h4 style="margin-top: 0; margin-bottom: 1rem; font-size: 0.9rem; text-transform: uppercase; color: var(--text-muted);">Bill Details</h4>
            
            <div class="bill-row">
                <span>Item Total</span>
                <span>₹${itemTotal.toFixed(2)}</span>
            </div>
            <div class="bill-row">
                <span>Platform Fee</span>
                <span>₹${platformFee.toFixed(2)}</span>
            </div>
            <div class="bill-row">
                <span>GST and Restaurant Charges</span>
                <span>₹${tax.toFixed(2)}</span>
            </div>
            
            <div class="bill-row total">
                <span>To Pay</span>
                <span>₹${finalTotal.toFixed(2)}</span>
            </div>
        </div>
    `;

    cartItemsContainer.innerHTML = itemsHtml + infoBanner + billDetails;
    document.getElementById('cart-total-amount').innerText = finalTotal.toFixed(2);
    // Also update the button amount
    const finalPaySpan = document.getElementById('final-pay-amount');
    if (finalPaySpan) finalPaySpan.innerText = finalTotal.toFixed(2);
}

function setupEventListeners() {
    const cartModal = document.getElementById('cart-modal');
    const cartBtn = document.getElementById('cart-toggle');
    const closeBtn = document.querySelector('.close-modal');
    const checkoutBtn = document.getElementById('checkout-btn');

    cartBtn.addEventListener('click', () => {
        cartModal.classList.add('active');
    });

    closeBtn.addEventListener('click', () => {
        cartModal.classList.remove('active');
    });

    window.onclick = function (event) {
        if (event.target == cartModal) {
            cartModal.classList.remove('active');
        }
    };

    checkoutBtn.addEventListener('click', processCheckout);
}

async function processCheckout() {
    const items = Object.values(cart).map(item => ({
        id: item.id,
        quantity: item.quantity
    }));

    if (items.length === 0) return;

    const checkoutBtn = document.getElementById('checkout-btn');
    const originalText = checkoutBtn.innerText;
    checkoutBtn.innerText = 'Processing Payment...';
    checkoutBtn.disabled = true;

    // Simulate payment delay
    await new Promise(r => setTimeout(r, 1500));

    const guestNameInput = document.getElementById('guest_name');
    let customerName = 'Guest';

    if (guestNameInput) {
        if (!guestNameInput.value.trim()) {
            alert("Please enter your name to proceed.");
            checkoutBtn.innerText = originalText;
            checkoutBtn.disabled = false;
            return;
        }
        customerName = guestNameInput.value.trim();
    }

    try {
        const response = await fetch('/api/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                items: items,
                customer_name: customerName
            })
        });

        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
            const result = await response.json();
            if (result.success) {
                // Save to LocalStorage
                const existing = localStorage.getItem('canteen_orders');
                const orders = existing ? JSON.parse(existing) : [];
                orders.push(result.order_id);
                localStorage.setItem('canteen_orders', JSON.stringify(orders));

                window.location.href = `/order/${result.order_id}`;
                cart = {};
                updateCartUI();
            } else {
                alert('Order failed: ' + result.error);
            }
        } else {
            const text = await response.text();
            console.error("Server returned non-JSON response:", text);
            alert('Server Error: ' + text.substring(0, 100));
        }

    } catch (error) {
        console.error('Checkout error:', error);
        alert('Checkout failed. See console for details.');
    } finally {
        checkoutBtn.innerText = originalText;
        checkoutBtn.disabled = false;
    }
}

function showToast(message) {
    // Simple toast implementation could go here
    console.log(message);
}
