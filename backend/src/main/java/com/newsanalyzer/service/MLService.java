package com.newsanalyzer.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
@Slf4j
public class MLService {

    @Value("${ml.service.url:http://ml-service:5000}")
    private String mlServiceUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    public Map<String, Object> predict(String text) {
        String url = mlServiceUrl + "/predict";
        log.info("Calling ML service at: {}", url);
        
        Map<String, String> request = Map.of("text", text);
        
        return restTemplate.postForObject(url, request, Map.class);
    }
}
