
const API_BASE_URL = "http://127.0.0.1:8000/api/v1";


// ==========================================
// Fetch Purchase Requests
// ==========================================

async function fetchPurchaseRequests() {
    const tableBody = document.getElementById("requests-table-body");

    try {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6">Loading requests...</td>
            </tr>
        `;

        const response = await fetch(`${API_BASE_URL}/requests`);

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const requests = await response.json();

        updateDashboardStatistics(requests);
        renderPurchaseRequests(requests);

    } catch (error) {
        console.error("Could not load purchase requests:", error);

        tableBody.innerHTML = `
            <tr>
                <td colspan="6">
                    Unable to load purchase requests.
                    Please check that the API is running.
                </td>
            </tr>
        `;
    }
}


// ==========================================
// Dashboard Statistics
// ==========================================

function updateDashboardStatistics(requests) {
    const total = requests.length;

    const pending = requests.filter(
        request => request.status === "PENDING"
    ).length;

    const approved = requests.filter(
        request => request.status === "APPROVED"
    ).length;

    const rejected = requests.filter(
        request => request.status === "REJECTED"
    ).length;

    document.getElementById("total-requests").textContent = total;
    document.getElementById("pending-requests").textContent = pending;
    document.getElementById("approved-requests").textContent = approved;
    document.getElementById("rejected-requests").textContent = rejected;
}


// ==========================================
// Currency Formatting
// ==========================================

function formatCurrency(amount, currency) {
    return new Intl.NumberFormat("en-ZA", {
        style: "currency",
        currency: currency
    }).format(Number(amount));
}


// ==========================================
// Approval Route Formatting
// ==========================================

function formatApprovalRoute(route) {
    const routes = {
        AUTOMATIC_ELIGIBILITY: "Automatic Eligibility",
        MANAGER: "Manager",
        MANAGER_AND_FINANCE: "Manager + Finance"
    };

    return routes[route] || route;
}


// ==========================================
// Render Purchase Requests
// ==========================================

function renderPurchaseRequests(requests) {
    const tableBody = document.getElementById("requests-table-body");

    if (requests.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6">No purchase requests found.</td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = requests.map(request => `
        <tr>
            <td>${escapeHTML(request.requester_name)}</td>
            <td>${escapeHTML(request.department)}</td>
            <td>${escapeHTML(request.title)}</td>
            <td>${formatCurrency(request.amount, request.currency)}</td>
            <td>${escapeHTML(formatApprovalRoute(request.approval_route))}</td>
            <td>
                <span class="status-badge status-${request.status.toLowerCase()}">
                    ${escapeHTML(request.status)}
                </span>
            </td>
        </tr>
    `).join("");
}


// ==========================================
// HTML Escaping
// ==========================================

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, character => {
        const entities = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        };

        return entities[character];
    });
}


// ==========================================
// Form Feedback
// ==========================================

function showFormMessage(message, type) {
    const messageElement = document.getElementById("form-message");

    messageElement.textContent = message;
    messageElement.className = `form-message ${type}`;
}


// ==========================================
// Submit Purchase Request
// ==========================================

async function submitPurchaseRequest(event) {
    event.preventDefault();

    const form = event.target;
    const submitButton = document.getElementById("submit-request-btn");

    const formData = new FormData(form);

    const purchaseRequest = {
        requester_name: formData.get("requester_name").trim(),
        department: formData.get("department").trim(),
        title: formData.get("title").trim(),
        description: formData.get("description").trim(),
        amount: Number(formData.get("amount")),
        currency: formData.get("currency")
    };

    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";

    try {
        const response = await fetch(`${API_BASE_URL}/requests`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(purchaseRequest)
        });

        const result = await response.json();

        if (!response.ok) {
            const errorMessage = Array.isArray(result.detail)
                ? result.detail.map(error => error.msg).join(", ")
                : result.detail || "Could not submit purchase request.";

            throw new Error(errorMessage);
        }

        const approvalRoute = formatApprovalRoute(result.approval_route);

        showFormMessage(
            `Purchase request submitted successfully! Approval route: ${approvalRoute}. Status: ${result.status}.`,
            "success"
        );

        form.reset();

        // Refresh dashboard with the newly created request.
        await fetchPurchaseRequests();

    } catch (error) {
        console.error("Could not submit purchase request:", error);

        showFormMessage(
            error.message || "Something went wrong. Please try again.",
            "error"
        );

    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Submit Request";
    }
}


// ==========================================
// Initialise Application
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    // Load existing purchase requests.
    fetchPurchaseRequests();

    // Connect the purchase request form.
    const purchaseRequestForm = document.getElementById(
        "purchase-request-form"
    );

    purchaseRequestForm.addEventListener(
        "submit",
        submitPurchaseRequest
    );

});
