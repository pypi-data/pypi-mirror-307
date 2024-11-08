# EnvCrypted

EnvCrypted is a high-performance Python 3.12+ package that encrypts all environment variables using age encryption with ephemeral keys generated at runtime. It seamlessly integrates by monkey-patching `os.getenv` to return decrypted values, while ensuring that all other access methods yield encrypted data. Designed for efficiency, EnvCrypted operates with near-zero latency, making it ideal for performance-critical applications.

The package leverages Pyrage, the Python bindings for the Rust port of age, to provide robust encryption capabilities. Additionally, EnvCrypted offers optional integration with Pydantic Settings and 1Password through the latest onepassword-sdk package, enhancing its versatility in secure environments by leveraging 1Password Service Accounts as a Pydantic Settings Source.

**Note: This package is highly experimental!**

## License

This package is licensed under the [Apache 2.0](./LICENSE.txt) license.

EnvCrypted is not affiliated with 1Password, Pydantic, or any other projects, services, or entities referenced or depended upon by this package.
