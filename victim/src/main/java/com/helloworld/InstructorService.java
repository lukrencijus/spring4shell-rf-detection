package com.helloworld;

import org.springframework.data.domain.Page;
import java.util.List;

public interface InstructorService {

    List<Instructor> getAllInstructors();

    void saveInstructor(Instructor instructor);

    Instructor getInstructorById(long id);

    void deleteInstructorById(long id);

    Page<Instructor> findPaginated(int pageNum, int pageSize, String sortField, String sortDirection);
}
