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
        internal_api_token: &str,
        internal_workspace_id: &str,
    ) -> Box<dyn AiProvider> {
        match provider {
            "internal" => Box::new(InternalProvider::new(
                internal_api_url,
                internal_api_token,
                internal_workspace_id,
            )),
            _ => Box::new(OllamaProvider::new(ollama_base_url, ollama_model)),
        }
    }
}
