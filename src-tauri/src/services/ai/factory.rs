use super::internal_provider::InternalProvider;
use super::ollama_provider::OllamaProvider;
use super::provider::AiProvider;

pub struct AiProviderFactory;

impl AiProviderFactory {
    pub fn from_settings(
        provider: &str,
        ollama_base_url: &str,
        ollama_model: &str,
        internal_api_url: &str,
    ) -> Box<dyn AiProvider> {
        match provider {
            "internal" => Box::new(InternalProvider::new(internal_api_url)),
            _ => Box::new(OllamaProvider::new(ollama_base_url, ollama_model)),
        }
    }
}
