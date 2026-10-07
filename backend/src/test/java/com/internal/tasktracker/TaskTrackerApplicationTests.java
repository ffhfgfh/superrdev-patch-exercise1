package com.internal.tasktracker;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.hamcrest.Matchers.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class TaskTrackerApplicationTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private TaskRepository taskRepository;

    @Test
    @DisplayName("SQL Query should not return archived tasks when matching description")
    void testArchivedTasksExcludedOnSearch() {
        // "api" appears in description of archived tasks (e.g. Decommission legacy search endpoint)
        List<Task> results = taskRepository.searchTasks("%api%", null);
        for (Task task : results) {
            assertFalse(task.isArchived(), "Archived task found in search results: " + task.getTitle());
        }
    }

    @Test
    @DisplayName("SQL Query should respect status filter even when title matches search term")
    void testStatusFilterHonoredWhenTitleMatches() {
        // "Fix" appears in titles of OPEN, IN_PROGRESS, and DONE tasks
        List<Task> doneResults = taskRepository.searchTasks("%fix%", "DONE");
        assertFalse(doneResults.isEmpty(), "Should find DONE tasks matching 'fix'");
        for (Task task : doneResults) {
            assertEquals("DONE", task.getStatus(), "Non-DONE task returned with status=DONE filter");
            assertFalse(task.isArchived());
        }
    }

    @Test
    @DisplayName("API returns 200 with proper payload structure")
    void testSearchTasksEndpoint() throws Exception {
        mockMvc.perform(get("/api/tasks")
                .param("q", "api")
                .param("page", "1")
                .param("pageSize", "5"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.page").value(1))
                .andExpect(jsonPath("$.pageSize").value(5))
                .andExpect(jsonPath("$.total").isNumber())
                .andExpect(jsonPath("$.items").isArray());
    }

    @Test
    @DisplayName("API returns 400 Bad Request for invalid status")
    void testInvalidStatusReturnsBadRequest() throws Exception {
        mockMvc.perform(get("/api/tasks")
                .param("status", "NOT_A_VALID_STATUS"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").exists());
    }

    @Test
    @DisplayName("API handles page <= 0 gracefully")
    void testInvalidPageHandledGracefully() throws Exception {
        mockMvc.perform(get("/api/tasks")
                .param("page", "0")
                .param("pageSize", "5"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.page").value(1));
    }
}
