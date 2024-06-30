package examples;

public final class PrivateConfig {
    private PrivateConfig() {
    }
    public static final String BASE_URL = "https://testnet.binance.vision";

    public static final String API_KEY = "BKVGi487lFCsPvtSHR1GxI73URGhiJiN8AsmrobLCShlQE4xRATzkhMNIa6sqppb";
    public static final String SECRET_KEY = "o8WmykY91xUJMGtCwCeZ2cUj5yPnqluj44CJbOwsUHIflGhBAV5dYFgmeMj4oFDx"; // Unnecessary if PRIVATE_KEY_PATH is used
    public static final String PRIVATE_KEY_PATH = ""; // Key must be PKCS#8 standard

    public static final String TESTNET_API_KEY = "Jwp1egxRUNEHaPKJIoXCJR9SUfnU2qMcRJ2mzSHde3mOzPawJEioFLhyaYWOuJZb";
    public static final String TESTNET_SECRET_KEY = "IR1eqjbtoLt9kYq97C2SySU77bqqZQCHc7Dl46ii4WIPnYNiMlYSwXZDcCo26LYC"; // Unnecessary if TESTNET_PRIVATE_KEY_PATH is used
    public static final String TESTNET_PRIVATE_KEY_PATH = ""; //Key must be PKCS#8 standard
}
