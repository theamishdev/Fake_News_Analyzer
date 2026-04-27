package com.newsanalyzer.controller;

import com.newsanalyzer.service.MLService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/news")
@CrossOrigin(origins = "*")
@Slf4j
public class NewsController {

    @Autowired
    private MLService mlService;

    @PostMapping("/analyze")
    public ResponseEntity<?> analyzeNews(@RequestBody Map<String, String> request) {
        String text = request.get("text");
        if (text == null || text.isEmpty()) {
            return ResponseEntity.badRequest().body(Map.of("error", "Text is required"));
        }

        log.info("Request received to analyze news snippet");
        
        try {
            Map<String, Object> result = mlService.predict(text);
            log.info("Analysis completed successfully: {}", result.get("result"));
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            log.error("Error calling ML microservice: {}", e.getMessage());
            return ResponseEntity.status(503).body(Map.of(
                "error", "ML service is currently unavailable",
                "details", e.getMessage()
            ));
        }
    }

    @GetMapping("/health")
    public ResponseEntity<?> healthCheck() {
        return ResponseEntity.ok(Map.of("status", "UP"));
    }
}
