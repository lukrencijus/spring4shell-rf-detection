package com.helloworld;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/instructors")
public class InstructorController {
    
    @Autowired
    private InstructorService instructorService;
    
    @GetMapping("/")
    public String viewHomePage(Model model) {
        return findPaginated(1, "instructorName", "asc", model);
    }
    
    @GetMapping("/add")
    public String showNewInstructorForm(Model model) {
        Instructor instructor = new Instructor();
        model.addAttribute("instructor", instructor);
        return "instructor/new_instructor";
    }
    
    // Vulnerable method
    @PostMapping("/save")
    public String saveInstructor(@ModelAttribute("instructor") Instructor instructor) {
        instructorService.saveInstructor(instructor);
        return "redirect:/instructors/";
    }
    
    @GetMapping("/update/{id}")
    public String showFormForUpdate(@PathVariable(value = "id") long id, Model model) {
        Instructor instructor = instructorService.getInstructorById(id);
        model.addAttribute("instructor", instructor);
        return "instructor/update_instructor";
    }
    
    @GetMapping("/delete/{id}")
    public String deleteInstructor(@PathVariable(value = "id") long id) {
        this.instructorService.deleteInstructorById(id);
        return "redirect:/instructors/";
    }
    
    @GetMapping("/page/{pageNo}")
    public String findPaginated(@PathVariable(value = "pageNo") int pageNo,
                                @RequestParam("sortField") String sortField,
                                @RequestParam("sortDir") String sortDir,
                                Model model) {
        int pageSize = 5;
        
        Page<Instructor> page = instructorService.findPaginated(pageNo, pageSize, sortField, sortDir);
        List<Instructor> listInstructors = page.getContent();
        
        model.addAttribute("currentPage", pageNo);
        model.addAttribute("totalPages", page.getTotalPages());
        model.addAttribute("totalItems", page.getTotalElements());
        model.addAttribute("sortField", sortField);
        model.addAttribute("sortDir", sortDir);
        model.addAttribute("reverseSortDir", sortDir.equals("asc") ? "desc" : "asc");
        model.addAttribute("listInstructors", listInstructors);
        
        return "instructor/index";
    }
}
