package com.helloworld;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/departments")
public class DepartmentController {
    
    @Autowired
    private DepartmentService departmentService;
    
    @GetMapping("/")
    public String viewHomePage(Model model) {
        return findPaginated(1, "departmentName", "asc", model);
    }
    
    @GetMapping("/add")
    public String showNewDepartmentForm(Model model) {
        Department department = new Department();
        model.addAttribute("department", department);
        return "department/new_department";
    }
    
    // Vulnerable method
    @PostMapping("/save")
    public String saveDepartment(@ModelAttribute("department") Department department) {
        departmentService.saveDepartment(department);
        return "redirect:/departments/";
    }
    
    @GetMapping("/update/{id}")
    public String showFormForUpdate(@PathVariable(value = "id") long id, Model model) {
        Department department = departmentService.getDepartmentById(id);
        model.addAttribute("department", department);
        return "department/update_department";
    }
    
    @GetMapping("/delete/{id}")
    public String deleteDepartment(@PathVariable(value = "id") long id) {
        this.departmentService.deleteDepartmentById(id);
        return "redirect:/departments/";
    }
    
    @GetMapping("/page/{pageNo}")
    public String findPaginated(@PathVariable(value = "pageNo") int pageNo,
                                @RequestParam("sortField") String sortField,
                                @RequestParam("sortDir") String sortDir,
                                Model model) {
        int pageSize = 5;
        
        Page<Department> page = departmentService.findPaginated(pageNo, pageSize, sortField, sortDir);
        List<Department> listDepartments = page.getContent();
        
        model.addAttribute("currentPage", pageNo);
        model.addAttribute("totalPages", page.getTotalPages());
        model.addAttribute("totalItems", page.getTotalElements());
        model.addAttribute("sortField", sortField);
        model.addAttribute("sortDir", sortDir);
        model.addAttribute("reverseSortDir", sortDir.equals("asc") ? "desc" : "asc");
        model.addAttribute("listDepartments", listDepartments);
        
        return "department/index";
    }
}
