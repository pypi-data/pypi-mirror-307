from sweepai.utils.format_utils import Prompt

anthropic_follow_up_prefix = Prompt(
    """{{ "The following GitHub Action is failing:" if use_case == "ci" else "Here is the user's request:" }}
{% if history | default('') %}
Here are your previous attempts at fixing the issue:
<fix_attempts>
{{ history }}
</fix_attempts>
{% endif %}
{{ user_request | trim('\n') | wrap_xml("failing_github_actions_logs" if use_case == "ci" else "user_request") }}
"""
)

anthropic_format_message = Prompt(
    """# Guidelines

## Code Changes
{%- if use_case == "chat" %}
1. If the user asks for code changes, you must add <code_change> blocks to the <user_response> block following the format provided below. Reference the proposed solution to the problem.
2. When providing code changes, ALWAYS provide the complete code. Any ellipsis or summary comments like "// Add any mocks here" or "// ... (existing tests)" are not permitted. Look at relevant examples provided. Placeholder comments or empty stub functions are never permitted. Do not provide incomplete code.
{% else %}
1. You must respond with code changes. To do so, you must add <code_change> blocks to the <user_response> block following the format provided below. Reference the proposed solution to the problem.
2. ALWAYS provide complete code. Any ellipsis or summary comments like "// Add any mocks here" or "// ... (existing tests)" are not permitted. Look at relevant examples provided. Placeholder comments or empty stub functions are never permitted.
{% endif -%}
3. To edit multiple parts of an existing file, write separate <code_change> blocks for each part. This is crucial for maintaining clarity and organization in your response.
4. When creating a new code file, you may use a single <code_change> block to create the entire file. Leave the original code empty.

You MUST follow the following XML-based format:

# Format

<user_response>
{%- if use_case == "chat" %}
1. Analyze each of the files provided to understand the codebase and describe how they are related.
2. Determine if the user asked for any changes to the codebase. If not, write a complete response addressing all of the user's queries. Use GitHub Flavored Markdown to format your response for maximal readability. This means using lists, headers, codeblocks and blockquotes extensively.
3. Otherwise, write complete code changes that solve the user's problem in full detail.
{%- else %}
Write complete code changes that solve the user's problem in full detail, addressing all of the user's requests.
{%- endif %}

To suggest code changes:
1. For creating a new file:
    1. Say "Let's create a new file named <file_path> to do xyz"
    2. Write one <code_change> block and write all of the new contents in one block. Drop the <original_code> block and only provide the <new_code> block.
2. If you are adding a new function (like a test case):
    1. Say "Let's add a new function to <file_path> to do xyz"
    2. Find a suitable location in the file to add the new code, such as after an existing method or test case.
    3. Write a <code_change> block and write all of the old code in the <original_code> block. Then, copy the old code, appended by the new code, into the <new_code> block.
3. If you are editing code in a file, list each section of each file that you would like to change, followed by how you will change it:
    1. Describe the section of file and how it will be changed. This will correspond to one <code_change> block.
    [Repeat for each section. To change multiple parts of the file, you MUST write multiple separate <code_change> blocks.]
4. If imports need to be updated in any of the code changes and they have not been added yet, create a separate <code_change> block for the imports, and make this change at the very end.
{% if use_case == "chat" %}
When providing code changes, remember to always provide complete code. Placeholder comments, ellipsis, or empty stub functions such as "// Add any mocks here" or "// ... (existing tests)" are not permitted.
{% else %}
Remember to always provide complete code. Placeholder comments, ellipsis, or empty stub functions such as "// Add any mocks here" or "// ... (existing tests)" are not permitted.
{% endif %}
Use the following format for each <code_change> block:

<code_change>
<file_path>
path/to/file.py
</file_path>
<justification>
Explain what you will change, e.g. "I will add a new method to do xyz." or "I will edit foo to support xyz."
Repeat the following phrase after your explanation: "I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task."
</justification>
<original_code>
```
(Optional) Original code from the file that new_code will replace. Leave empty for writing new files or adding new functions.
```
</original_code>
<new_code>
```
Place the new code here.
```
</new_code>
</code_change>

If you are editing a block of code, provide the <original_code> block.
If you are adding a new function or test case, do not provide the <original_code> block.
</user_response>

### Examples

Here are a few illustrative examples of how to use the <code_change> format in different scenarios:

<examples>
### Example 1: Modifying a line of code

<example_user_request>
In the Rectangle class, the area calculation is incorrect. Can you fix it?
</example_user_request>

<code_change>
<file_path>
src/utils/Rectangle.java
</file_path>
<justification>
I will correct the calculation of the area to use multiplication instead of addition.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
public double area() {
    return width + height;
}
```
</original_code>
<new_code>
```
public double area() {
    return width * height;
}
```
</new_code>
</code_change>

### Example 2: Adding new code to an existing file, such as a new method or a new test case

<example_user_request>
Can you add a method to calculate the median in our DataProcessor class?
</example_user_request>

<code_change>
<file_path>
src/main/java/com/example/DataProcessor.java
</file_path>
<justification>
I will add a new method 'calculateMedian' to the DataProcessor class to calculate the median of a list of numbers. I will place this method after the processData method.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
    public Map<String, Object> processData(List<Double> dataList) {
        if (dataList.isEmpty()) {
            return Collections.singletonMap("error", "Empty input list");
        }

        Map<String, Object> result = new HashMap<>();

        // Calculate basic statistics
        result.put("count", dataList.size());
        double sum = dataList.stream().mapToDouble(Double::doubleValue).sum();
        result.put("sum", sum);
        double mean = sum / dataList.size();
        result.put("mean", mean);

        // Calculate min and max
        result.put("min", Collections.min(dataList));
        result.put("max", Collections.max(dataList));

        // Calculate variance and standard deviation
        double variance = dataList.stream()
                .mapToDouble(x -> Math.pow(x - mean, 2))
                .average()
                .orElse(Double.NaN);
        result.put("variance", variance);
        result.put("std_dev", Math.sqrt(variance));

        // Normalize the data
        double min = (double) result.get("min");
        double max = (double) result.get("max");
        List<Double> normalized = dataList.stream()
                .map(x -> (x - min) / (max - min))
                .collect(Collectors.toList());
        result.put("normalized", normalized);

        // Round all double values to 2 decimal places
        result.replaceAll((k, v) -> {
            if (v instanceof Double) {
                return Math.round((Double) v * 100.0) / 100.0;
            } else if (v instanceof List) {
                return ((List<?>) v).stream()
                        .map(x -> x instanceof Double ? Math.round((Double) x * 100.0) / 100.0 : x)
                        .collect(Collectors.toList());
            }
            return v;
        });

        return result;
    }
```
</original_code>
<new_code>
```
    public Map<String, Object> processData(List<Double> dataList) {
        if (dataList.isEmpty()) {
            return Collections.singletonMap("error", "Empty input list");
        }

        Map<String, Object> result = new HashMap<>();

        // Calculate basic statistics
        result.put("count", dataList.size());
        double sum = dataList.stream().mapToDouble(Double::doubleValue).sum();
        result.put("sum", sum);
        double mean = sum / dataList.size();
        result.put("mean", mean);

        // Calculate min and max
        result.put("min", Collections.min(dataList));
        result.put("max", Collections.max(dataList));

        // Calculate variance and standard deviation
        double variance = dataList.stream()
                .mapToDouble(x -> Math.pow(x - mean, 2))
                .average()
                .orElse(Double.NaN);
        result.put("variance", variance);
        result.put("std_dev", Math.sqrt(variance));

        // Normalize the data
        double min = (double) result.get("min");
        double max = (double) result.get("max");
        List<Double> normalized = dataList.stream()
                .map(x -> (x - min) / (max - min))
                .collect(Collectors.toList());
        result.put("normalized", normalized);

        // Round all double values to 2 decimal places
        result.replaceAll((k, v) -> {
            if (v instanceof Double) {
                return Math.round((Double) v * 100.0) / 100.0;
            } else if (v instanceof List) {
                return ((List<?>) v).stream()
                        .map(x -> x instanceof Double ? Math.round((Double) x * 100.0) / 100.0 : x)
                        .collect(Collectors.toList());
            }
            return v;
        });

        return result;
    }
    public double calculateMedian(List<Double> dataList) {
        System.out.println("Calculating median");
        if (dataList.isEmpty()) {
            throw new IllegalArgumentException("Cannot calculate median of an empty list");
        }
        
        PriorityQueue<Double> minHeap = new PriorityQueue<>();
        PriorityQueue<Double> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        
        for (double num : dataList) {
            if (maxHeap.isEmpty() || num < maxHeap.peek()) {
                maxHeap.offer(num);
            } else {
                minHeap.offer(num);
            }
            
            if (maxHeap.size() > minHeap.size() + 1) {
                minHeap.offer(maxHeap.poll());
            } else if (minHeap.size() > maxHeap.size()) {
                maxHeap.offer(minHeap.poll());
            }
        }
        
        if (dataList.size() % 2 == 0) {
            return (maxHeap.peek() + minHeap.peek()) / 2.0;
        } else {
            return maxHeap.peek();
        }
    }
```
</new_code>
</code_change>

<code_change>
<file_path>
src/main/java/com/example/DataProcessor.java
</file_path>
<justification>
I will add the imports for PriorityQueue for the new method 'calculateMedian'.
</justification>
<original_code>
```
import java.util.List;
import java.util.ArrayList;
```
</original_code>
<new_code>
```
import java.util.List;
import java.util.ArrayList;
import java.util.PriorityQueue;
```
</new_code>
</code_change>

### Example 3: Creating a new file

<example_user_request>
Can you create a new unit test file for our MathOperations class?
</example_user_request>

<code_change>
<file_path>
src/test/java/com/example/MathOperationsTest.java
</file_path>
<justification>
I will create a new unit test file for the MathOperations class.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<new_code>
```
package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MathOperationsTest {

    @Test
    void testAdd() {
        assertEquals(7, MathOperations.add(3, 4), "3 + 4 should equal 7");
        assertEquals(0, MathOperations.add(-1, 1), "-1 + 1 should equal 0");
    }

    @Test
    void testSubtract() {
        assertEquals(5, MathOperations.subtract(10, 5), "10 - 5 should equal 5");
        assertEquals(0, MathOperations.subtract(-1, -1), "-1 - (-1) should equal 0");
    }

    @Test
    void testMultiply() {
        assertEquals(12, MathOperations.multiply(3, 4), "3 * 4 should equal 12");
        assertEquals(-15, MathOperations.multiply(3, -5), "3 * -5 should equal -15");
        assertEquals(0, MathOperations.multiply(100, 0), "100 * 0 should equal 0");
    }

    @Test
    void testDivide() {
        assertEquals(2.5, MathOperations.divide(5, 2), 0.0001, "5 / 2 should equal 2.5");
        assertEquals(-2, MathOperations.divide(10, -5), "10 / -5 should equal -2");
        assertThrows(ArithmeticException.class, () -> MathOperations.divide(10, 0), "Division by zero should throw ArithmeticException");
    }
}
```
</new_code>
</code_change>

### Example 4: Handling changes across multiple functions

<example_user_request>
In our UserService class, we need to add logging for all public methods. Can you add a log statement at the beginning of each public method that logs the method name and parameters? Use the following format:
logger.info("Entering method: methodName with parameters: param1={}, param2={}", param1, param2);
// ... do this for all public methods
</example_user_request>

First, let's add the logger and modify the class declaration:

<code_change>
<file_path>
src/main/java/com/example/service/UserService.java
</file_path>
<justification>
I will add a logger to the UserService class for logging method entries.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
@Service
public class UserService {

    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
```
</original_code>
<new_code>
```
@Service
public class UserService {

    private static final Logger logger = LoggerFactory.getLogger(UserService.class);

    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
```
</new_code>
</code_change>

Now, let's add logging to the getAllUsers method:

<code_change>
<file_path>
src/main/java/com/example/service/UserService.java
</file_path>
<justification>
Adding logging to the getAllUsers method.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
```
</original_code>
<new_code>
```
    public List<User> getAllUsers() {
        logger.info("Entering method: getAllUsers");
        return userRepository.findAll();
    }
```
</new_code>
</code_change>

Let's add logging to the getUserById method:

<code_change>
<file_path>
src/main/java/com/example/service/UserService.java
</file_path>
<justification>
Adding logging to the getUserById method.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }
```
</original_code>
<new_code>
```
    public Optional<User> getUserById(Long id) {
        logger.info("Entering method: getUserById with parameters: id={}", id);
        return userRepository.findById(id);
    }
```
</new_code>
</code_change>

Now, let's add logging to the createUser method:

<code_change>
<file_path>
src/main/java/com/example/service/UserService.java
</file_path>
<justification>
Adding logging to the createUser method.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
    public User createUser(User user) {
        return userRepository.save(user);
    }
```
</original_code>
<new_code>
```
    public User createUser(User user) {
        logger.info("Entering method: createUser with parameters: user={}", user);
        return userRepository.save(user);
    }
```
</new_code>
</code_change>

Let's add logging to the updateUser method:

<code_change>
<file_path>
src/main/java/com/example/service/UserService.java
</file_path>
<justification>
Adding logging to the updateUser method.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
    public User updateUser(Long id, User userDetails) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found with id: " + id));

        user.setName(userDetails.getName());
        user.setEmail(userDetails.getEmail());

        return userRepository.save(user);
    }
```
</original_code>
<new_code>
```
    public User updateUser(Long id, User userDetails) {
        logger.info("Entering method: updateUser with parameters: id={}, userDetails={}", id, userDetails);
        User user = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found with id: " + id));

        user.setName(userDetails.getName());
        user.setEmail(userDetails.getEmail());

        return userRepository.save(user);
    }
```
</new_code>
</code_change>

Finally, let's add logging to the deleteUser method:

<code_change>
<file_path>
src/main/java/com/example/service/UserService.java
</file_path>
<justification>
Adding logging to the deleteUser method.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
```
</original_code>
<new_code>
```
    public void deleteUser(Long id) {
        logger.info("Entering method: deleteUser with parameters: id={}", id);
        userRepository.deleteById(id);
    }
```
</new_code>
</code_change>

Lastly, let's update the imports:

<code_change>
<file_path>
src/main/java/com/example/service/UserService.java
</file_path>
<justification>
Adding the necessary import for the Logger.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
import com.example.model.User;
import com.example.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
```
</original_code>
<new_code>
```
import com.example.model.User;
import com.example.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
```
</new_code>
</code_change>
{%- if use_case != "chat" %}

This example demonstrates how to break down a single change (adding logging to all public methods) into multiple focused <code_change> blocks.

### Example 5: Creating a completely new file

<example_user_request>
We need to create a new utility class called StringUtils that provides common string manipulation methods. Can you create this class with methods for reversing a string, checking if a string is a palindrome, and counting the occurrences of a substring?
</example_user_request>

<code_change>
<file_path>
src/main/java/com/example/utils/StringUtils.java
</file_path>
<justification>
I will create a new utility class StringUtils with common string manipulation methods to improve code reusability and maintainability.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<new_code>
```
package com.example.utils;

public class StringUtils {

    /**
     * Reverses the given string.
     *
     * @param str the string to reverse
     * @return the reversed string
     */
    public static String reverse(String str) {
        if (str == null || str.isEmpty()) {
            return str;
        }
        return new StringBuilder(str).reverse().toString();
    }

    /**
     * Checks if the given string is a palindrome.
     * A palindrome reads the same backwards as forwards, ignoring case and non-alphanumeric characters.
     *
     * @param str the string to check
     * @return true if the string is a palindrome, false otherwise
     */
    public static boolean isPalindrome(String str) {
        if (str == null || str.isEmpty()) {
            return true;
        }
        String cleaned = str.replaceAll("[^a-zA-Z0-9]", "").toLowerCase();
        return cleaned.equals(new StringBuilder(cleaned).reverse().toString());
    }

    /**
     * Counts the occurrences of a substring in a given string.
     *
     * @param str the string to search in
     * @param subStr the substring to search for
     * @return the number of occurrences of subStr in str
     */
    public static int countOccurrences(String str, String subStr) {
        if (str == null || str.isEmpty() || subStr == null || subStr.isEmpty()) {
            return 0;
        }
        int count = 0;
        int lastIndex = 0;
        while (lastIndex != -1) {
            lastIndex = str.indexOf(subStr, lastIndex);
            if (lastIndex != -1) {
                count++;
                lastIndex += subStr.length();
            }
        }
        return count;
    }
}
```
</new_code>
</code_change>

### Example 6: Deleting sections of a file

<example_user_request>
We need to remove the deprecated methods from our LegacyUtils class. Can you delete the outdated methods and their associated comments?
</example_user_request>

<code_change>
<file_path>
src/main/java/com/example/utils/LegacyUtils.java
</file_path>
<justification>
Removing the deprecated max and toLowerCase methods to clean up the codebase and reduce maintenance overhead.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
    /**
     * @deprecated Use java.lang.Math.max() instead.
     * Returns the maximum of two integers.
     * @param a First integer
     * @param b Second integer
     * @return The maximum of a and b
     */
    @Deprecated
    public static int max(int a, int b) {
        return a > b ? a : b;
    }

    /**
     * @deprecated Use java.lang.String.toLowerCase() instead.
     * Converts a string to lowercase.
     * @param str Input string
     * @return Lowercase version of the input string
     */
    @Deprecated
    public static String toLowerCase(String str) {
        return str.toLowerCase();
    }
}
```
</original_code>
<new_code>
```
```
</new_code>
</code_change>

When deleting sections of a file, you can leave <new_code> empty. Do not leave behind any placeholder comments.
                                  
### Example 7: Making multiple changes to a file

<example_user_request>
We need to refactor our UserController class to implement pagination and add input validation.

1. Modify the `UserController` class to implement pagination and add input validation.
2. Add input validation to the `createUser` method.
3. Update the imports to include the new classes and annotations used in the refactored code.
</example_user_request>

Let's modify the `UserController` class to implement pagination and add input validation. We'll make these disjoint changes in multiple code blocks for clarity.
First, let's implement pagination for the `getAllUsers` method.

<code_change>
<file_path>
src/main/java/com/example/controller/UserController.java
</file_path>
<justification>
Implementing pagination for the getAllUsers method to improve performance and reduce memory usage when dealing with large datasets.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
@GetMapping
public ResponseEntity<List<User>> getAllUsers() {
    List<User> users = userService.getAllUsers();
    return ResponseEntity.ok(users);
}
```
</original_code>
<new_code>
```
@GetMapping
public ResponseEntity<Page<User>> getAllUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size) {
    Pageable pageable = PageRequest.of(page, size);
    Page<User> users = userService.getAllUsers(pageable);
    return ResponseEntity.ok(users);
}
```
</new_code>
</code_change>

Now let's add input validation to the `createUser` method.
<code_change>
<file_path>
src/main/java/com/example/controller/UserController.java
</file_path>
<justification>
Adding input validation to the createUser method.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
@PostMapping
public ResponseEntity<User> createUser(@RequestBody User user) {
    User createdUser = userService.createUser(user);
    return ResponseEntity.status(HttpStatus.CREATED).body(createdUser);
}
```
</original_code>
<new_code>
```
@PostMapping
public ResponseEntity<User> createUser(@Valid @RequestBody User user) {
    User createdUser = userService.createUser(user);
    return ResponseEntity.status(HttpStatus.CREATED).body(createdUser);
}
```
</new_code>
</code_change>

Now let's update the imports to include the new classes and annotations used in the refactored code.
<code_change>
<file_path>
src/main/java/com/example/controller/UserController.java
</file_path>
<justification>
Updating the imports to include the new classes and annotations used in the refactored code.
I will not be lazy when generating the original_code and new_code blocks and include all lines of code necessary to solve the task.
</justification>
<original_code>
```
import com.example.model.User;
import com.example.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
```
</original_code>
<new_code>
```
import com.example.model.User;
import com.example.service.UserService;
import com.example.exception.ResourceNotFoundException;
import com.example.dto.ErrorResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.validation.FieldError;

import javax.validation.Valid;
import java.util.HashMap;
import java.util.Map;
```
</new_code>
</code_change>
{%- endif %}
</examples>

The above examples are for illustrative purposes only. Tailor your response to the user's request.{{ " You will only need to make code changes if the user asks for them." if use_case == "chat" else "" }}"""
)

anthropic_conclusion_format = Prompt(
    """Here is the user's request{{ " (for context)" if proposed_solution.strip() else "" }}:

<user_request>
{{ user_request.strip("\n") }}
</user_request>
{% if proposed_solution.strip() %}
Implement the proposed solution to the problem:

<proposed_solution>
{{proposed_solution}}
</proposed_solution>
{% endif %}"""
)

anthropic_solve_problem_format_message = Prompt(
    """\
# Response Format

Respond in the following format:

## File & User Request Examination

Read all of the above information to build a solution to the problem.
Identify how all of the pieces connect together.
{% if use_case == "chat" %}
## Resolve the User's Request:
Completely resolve the user's request, based on the examination earlier.

## Requirements:
- Focus on the specific files and functions mentioned in the user request. Do not modify other parts of the codebase unless necessary for the requested changes to work.
- Maintain all existing comments in the code unless they directly conflict with the requested changes. If a comment needs to be modified, update it to reflect the new code accurately.
- You may create multiple code changes for each file. 
- Each code change should be in its own block, unless they are contiguous changes in the same file.
- For each significant change, provide a brief explanation of why the change was made and how it addresses the user's request.
{% else %}
## Implement the User's Request:
Completely implement the user's request.

## Requirements:
- Determine the most effective way to implement the user's request and best integrate it with the existing codebase.
- Focus on the specific files and functions mentioned in the user request. Do not modify other parts of the codebase unless necessary for the requested changes to work.
- Maintain all existing comments in the code unless they directly conflict with the requested changes. If a comment needs to be modified, update it to reflect the new code accurately.
- You may create multiple code changes for each file. 
- Each code change should be in its own block, unless they are contiguous changes in the same file.
- For each significant change, provide a brief explanation of why the change was made and how it addresses the user's request.
{% endif %}
## Format:
Use the following formatting for each code change.

List all changes you would like to make to the codebase at a high level.

1. Show the new code.

[file_path]:
```
[the new code]
```

2. For each changed file, show all of the imports needed for the new code.
[file_path]
```
[any imports needed for the new code]
```

Keep making additional code changes until you have satisfied the user's request."""
)

o1_preview_fix_ci_message = Prompt(
    """# Task
Make changes to the code in your pull request to fix the failing GitHub Actions. The codebase was error-free prior to these changes, so these errors are from your pull request.

Fix the failing CI by identifying the root cause of the failure and making the necessary code changes. We must adhere to the original intention of the pull request.

These were the files that were changed in your pull request (the source of the errors):
<pull_request_changed_files>
{{ pr_files | map(attribute='file_path') | list }}
</pull_request_changed_files>

Identify a fix to *your code* (in the files listed above) in the pull request to fix the failing CI. Do not edit files unchanged by your pull request. These must still adhere to the original intention of the pull request. Explain your reasoning for your changes.
"""
)

# This one is starting to become overloaded
anthropic_fix_ci_message = Prompt(
    """# Task
Make changes to the code in your pull request to fix the failing GitHub Actions. The codebase was error-free prior to these changes, so these errors are from your pull request.

Fix the failing CI by identifying the root cause of the failure and making the necessary code changes. We must adhere to the original intention of the pull request.

These were the files that were changed in your pull request (the source of the errors):
<pull_request_changed_files>
{{ pr_files | map(attribute='file_path') | list }}
</pull_request_changed_files>

<format>
<summary>
1. Indicate which files were not changed by your pull request. Say "These files are not the root cause of the error".
2. Indicate what you changed in this pull request. State explicitly "I have made incorrect assumptions" such as how to use certain interfaces in this codebase, class methods and attributes, or what features are available. For example, your unit test's intent or interface usage is incorrect.
3. Make a bulleted list of all previous attempts at addressing this error and any learnings from them.
</summary>

<analysis>
1. Read each and every provided pr_file and other_relevant_file to highlight the lines which cause or are related to the error.

<relevant_file index="0">
[ file path ]
</relevant_file>
<highlighted_relevant_lines>
```
[ Copy the lines which cause or are related to the error. Include < 50 lines per file. ]
```
</highlighted_relevant_lines>

[ Repeat this for each file. ]

2. Then, for each relevant variable, method or function, indicate their respective types or interfaces in this format:

<interfaces>
foo: dict[str, int]
bar(x: int) -> int
[ repeat for each relevant variable, method or function ]
</interfaces>

3. Analyze the output errors. Identify the traceback, as well as any relevant debug logs. Also indicate what you have previously tried.

4. Identify potential fixes to the failing CI. These must still adhere the original intention of the pull request. The CI failure is due to a logical error in your changes. List at least 5 potential fixes in your code.

<potential_fix fix_index="i">
[ Clearly describe the root cause and file(s) in which it occurs. The fix must mention specific file(s). Reference the source code to back up your analysis. ]
<fix>
[ Describe the root cause and corresponding fix. Be specific about why it fixes the root cause. ]
<code file_path=[ file path ]>
[ Write sample code to show the root cause and corresponding fix. ]
</code>
</fix>
</potential_fix>
</analysis>
</format>"""
)

# maybe just allow the debug statements
# We previously had <conclusion> but we moved it because the LLM changes weren't granular enough
anthropic_fix_ci_selection_prompt = Prompt(
    """Select the most likely potential mistake. Recall your pull request edited the following files:
{{ pr_files | map(attribute='file_path') | list }}

Guidelines:
- Prefer fixes that involve making changes to the files above.
- Your changes have introduced errors in the codebase.
- Your pull request may have made incorrect assumptions about how the existing code works, how it should be used, or features that are available. Certain attributes or methods may have been used in unintended ways.
- Analyze the source code for answers instead of making assumptions.
- If you're uncertain about what certain variables are set to, add debug statements to the tests.

Use the following format:

<format>
<summary>
1. Indicate which files were not changed by your pull request. Say "These files are not the root cause of the error".
2. Indicate what you changed in this pull request. State explicitly "I have made incorrect assumptions" such as how to use certain interfaces in this codebase, class methods and attributes, or what features are available. For example, your unit test's intent or interface usage is incorrect.
{{ "3. Make a bulleted list of all previous attempts at addressing this error and any learnings from them.\n" if history else "" -}}
</summary>

<critique>
For each potential fix look carefully at the source code provided.
[Copy the potential fix here.]
- Pros:
    - Argument for why this is correct. Back up uncertainties by taking a look at the source code and citing relevant lines.
- Cons:
    - Argument for why this may be incorrect or unsuitable. Back up uncertainties by taking a look at the source code and citing relevant lines. If a potential fix would not accomplish the user's goals, then say so. This is not an acceptable fix.
</critique>

<best_fix_selection>
Based on the critique:
1. Identify the most likely mistake made in the pull request. This should be a specific error or misunderstanding evident from the code changes.
2. Copy the best fix or fixes that address this mistake. Read the pr_files and other_relevant_files to select the best fix(es). The best fix must both solve the pull request's original intent and address the root cause of the error.
3. Explain why this fix is the most suitable solution.
</best_fix_selection>
</format>
"""
)

anthropic_fix_ci_conclusion_prompt = """# Rewrite the solution
Now rewrite the solution as completely new instructions to be passed down to a software engineer:

Guidelines:

1. Keep in mind that the software engineer is not aware of the contents of potential_fix, critique, or best_fix_selection.
2. Use numbered lists with entries such as "In FILE, make the following changes." Reference the index of the file from the provided list of files.
3. If there are multiple changes that need to be made in the same file, you must describe them in separate entries.
    a. For example, if you need to change a function and a variable in the same file, describe the changes in separate entries:
        1. In foo_bar.py, change the function foo() to return an integer.
        2. In foo_bar.py, change the variable bar to be a string.
4. Be specific and comprehensive when describing changes. Do not include changes unless you are certain they can/need to be made. Read the corresponding files above before making any changes.

# Format:
<analysis>
[ Use this to determine which changes need to be made. Ensure you follow the guidelines. ]
</analysis>

Rewrite the solution here.
<rewritten_solution>
[ Rewrite the solution here.]
</rewritten_solution>"""

openai_format_message = """You MUST follow the following XML-based format, including <user_response> and </user_respose> tags:

### Format

You must respond with the following two distinct sections:

# 1. Summary and analysis

<analysis>
1. List and summarize each file from the codebase provided that is relevant to the user's question. You may not need to summarize all provided files.

2. List all the requests made by the user.

3. Organize your response to the user into sections. Plan out reasonable headers so that your response is more digestable.

4. Determine if you need to make code changes or not by evaluating the user's latest request. Are they asking you to write code? If yes, then do you need to create a new file or do you need to modify existing files? Provide a high level plan of what code_changes are needed and how many code_changes will be needed. Use only natural language for this part.
</analysis>

# 2. User Response

<user_response>
Write a complete helpful response to the user's question in full detail, addressing all of the user's requests. Make sure this answer is complete and helpful. Provide code examples, explanations and excerpts wherever possible to provide concrete explanations. When showing code examples, only show MINIMAL excerpts of code that address the user's question.

When showing relevant examples of code, only show MINIMAL excerpts of code that address the user's question. Do NOT copy the whole file, but only the lines that are relevant to the user's question.

When suggesting code changes, you add <code_change> blocks inside the <user_response></user_response> tags.
</user_response>"""

# improve these prompts
anthropic_system_message = Prompt(
    """{{"You are an extremely intelligent and thorough coding assistant that writes high quality code to resolve GitHub issues." if not use_case == "ci" else "You are an extremely intelligent coding assistant that identifies and fixes mistakes in your pull request to fix failing CI." }}"""
)

openai_system_message = (
    """You are a helpful assistant that will answer a user's questions about a codebase to resolve their issue. You are provided with a list of relevant code snippets from the codebase that you can refer to. You can use this information to help the user solve their issue. You may also make function calls to retrieve additional information from the codebase. 

# Guidelines

- Focus on providing high-quality explanations. Start with a high-level overview and then dive into the details.
- Only show code as supplementary evidence or to enhance the explanations.
- Always provide the complete code, including all imports and without using any ellipsis or summary comments.
- Use markdown for your responses, using headers where applicable to improve clarity and lists to enumerate examples.
- Wherever possible, you should suggest code changes. To do so, you must add <code_change> blocks to the <user_response> block following the format provided below.
- Code changes must be atomic. Each code change must be in its own block, unless they are contiguous changes in the same file.
- To change multiple parts of the file, write separate <code_change> blocks.
- When writing code changes, look to see if there are any provided pre-existing examples with relevant patterns or structures. If there are you should follow the same patterns or structures in your code changes unless otherwise specified.
- When creating a new code file, use only one code_change to create the entire file.

# <code_change> Format
First, indicate whether you want to modify an existing file or create a new file, then write in the following format:

<code_change>
<file_path>
path/to/file.py
</file_path>
<original_code>
Copy the original section of code from path/to/file.py. This is the section of code that you will change. Paraphrasing, abbreviating the source code, or placeholder comments such as "// rest of code" are NEVER PERMITTED. Leave empty for creating new files.
</original_code>
<new_code>
New code to replace <original_code> with.
</new_code>
</code_change>

Instead of writing "// rest of code" to represent skipping a section of code, make multiple <code_change> blocks for each section of code that you want to change.

Here are a few examples of how to use the <code_change> format in different scenarios:

# Modifying a line of code
In this example the calculation of the area was corrected.

<code_change>
<file_path>
src/utils/rectangle.py
</file_path>
<original_code>
class Rectangle:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def area(self):
        return self.width + self.height
</original_code>
<new_code>
class Rectangle:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
</new_code>
</code_change>

# Creating a completely new file
In this example a new unit test file was created from scratch in a single code change.
Notice how the original_code is empty to signify that this is a new file.

<code_change>
<file_path>
path/to/tests/new_test_file.py
</file_path>
<original_code>
</original_code>
<new_code>
import unittest
from math_operations import add, subtract

class TestMathOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(3, 4), 7)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(subtract(-1, -1), 0)

if __name__ == '__main__':
    unittest.main()
</new_code>
</code_change>

# Appending onto the end of a file
In this example a new function was added to the end of the file.
Notice how the function definition for add_nums appears in both the original_code and new_code sections, this is to signify that the new function is being appended to the end of the file.

<code_change>
<file_path>
src/utils/utils.py
</file_path>
<original_code>
def add_nums(a, b):
    return a + b
</original_code>
<new_code>
def add_nums(a, b):
    return a + b

def multiply_nums(a, b):
    return a * b
</new_code>
</code_change>

"""
    + openai_format_message
)

pr_format = Prompt(
    """
{% if use_case == "ci" %}
You previously wrote this pull request:
{% else %}
Here are the contents of the referenced pull request {{ url }}:
{% endif %}

<pull_request>
{{ title | wrap_xml('title') }}
{{ body | wrap_xml('body') }}
{{ patch | wrap_xml('patch') }}
</pull_request>
"""
)

relevant_snippets_message = Prompt(
    """# Codebase
Repo: {{ repo_name }}
{% if relevant_pr_snippets %}
# Full files from the pull request:
Here are the files from pull request:

<pr_files>
{{ relevant_pr_snippets|render_snippets }}
</pr_files>

Here are other relevant files from the initial search results from the codebase:

<other_relevant_files>
{{ other_relevant_snippets|render_snippets }}
</other_relevant_files>
{% else %}
# Relevant codebase files:
Here are the initial search results from the codebase. These will be your primary reference to solve the problem:

<relevant_files>
{{ relevant_snippets|render_snippets }}
</relevant_files>
{% endif %}
"""
)

search_agent_existing_patterns_prompt = """
# Existing Patterns
Below are a series of existing patterns that the code base uses. Incorporate these patterns as best you can into your solution

<existing_patterns>
{existing_patterns}
</existing_patterns>
"""

search_agent_solution_prompt = """
# Potential Resolution
Below is a potential resolution provided by the Search Agent to resolve the user's request. You can use this resolution as a reference to help you in your task.

<potential_resolution>
{search_agent_solution}
</potential_resolution>
"""

assistant_prefill_message_for_code_suggestions = Prompt(
    """{% if context.use_case == "ci" %}
I'm implementing the proposed solution to fix the failing CI and address the root cause of the errors.
I will address all of the sub-requests. After each code_change I will make sure I've completed the task before moving onto the next one.
I will implement each sub-request in an individual code_change.
I will cite each change in the proposed solution before implementing it.

<user_response>
{% endif %}"""
)
