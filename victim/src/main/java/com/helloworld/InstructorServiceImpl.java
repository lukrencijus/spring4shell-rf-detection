package com.helloworld;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class InstructorServiceImpl implements InstructorService {
    
    @Autowired
    private InstructorRepository instructorRepository;
    
    @Override
    public List<Instructor> getAllInstructors() {
        return instructorRepository.findAll();
    }
    
    @Override
    public void saveInstructor(Instructor instructor) {
        this.instructorRepository.save(instructor);
    }
    
    @Override
    public Instructor getInstructorById(long id) {
        Optional<Instructor> optional = instructorRepository.findById(id);
        Instructor instructor = null;
        if (optional.isPresent()) {
            instructor = optional.get();
        } else {
            throw new RuntimeException("Instructor not found for id : " + id);
        }
        return instructor;
    }
    
    @Override
    public void deleteInstructorById(long id) {
        this.instructorRepository.deleteById(id);
    }
    
    @Override
    public Page<Instructor> findPaginated(int pageNum, int pageSize, String sortField, String sortDirection) {
        Sort sort = sortDirection.equalsIgnoreCase(Sort.Direction.ASC.name()) ? 
                Sort.by(sortField).ascending() : 
                Sort.by(sortField).descending();
        
        Pageable pageable = PageRequest.of(pageNum - 1, pageSize, sort);
        return this.instructorRepository.findAll(pageable);
    }
}
